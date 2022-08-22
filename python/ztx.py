#!/usr/bin/env python3

class Reader:
	def __init__(self, data):
		self.data = data
		self.index = 0

	def remaining(self):
		return len(self.data) - self.index

	def get(self, n):
		result = self.data[self.index:self.index+n]
		self.index += n
		return result

	def compact(self):
		b0 = self.get(1)[0]
		if b0 < 253:
			return b0
		elif b0 == 253:
			return int.from_bytes(self.get(2), "little")
		elif b0 == 254:
			return int.from_bytes(self.get(4), "little")
		elif b0 == 255:
			return int.from_bytes(self.get(8), "little")

	def uint32(self):
		return int.from_bytes(self.get(4), "little")

	def uint64(self):
		return int.from_bytes(self.get(8), "little")

	def sint64(self):
		return int.from_bytes(self.get(8), "little", signed=True)

def parse_tx(r):
	return dict([
		("header", parse_header(r)),
		("transparent", parse_transparent(r)),
		("sapling", parse_sapling(r)),
		("orchard", parse_orchard(r)),
	])

def parse_header(r):
	return dict([
		("version", r.uint32() ^ (1<<31)),
		("nVersionGroupId", r.get(4).hex()),
		("nConsensusBranchId", r.get(4).hex()),
		("lock_time", r.get(4).hex()),
		("nExpiryHeight", r.get(4).hex()),
	])

def parse_transparent(r):
	w = dict()
	nvin = r.compact()
	w["inputs"] = [parse_t_input(r) for _ in range(nvin)]
	nvout = r.compact()
	w["outputs"] = [parse_t_output(r) for _ in range(nvout)]
	return w

def parse_script(r):
	script_len = r.compact()
	return r.get(script_len)

def parse_t_input(r):
	return dict([
		("prevout", r.get(32).hex()),
		("previndex", r.uint32()),
		("sig_script", parse_script(r).hex()[:20]+"..."),
		("sequence", r.get(4).hex())
	])

def parse_t_output(r):
	return dict([
		("amount", r.uint64()),
		("pub_key_script", parse_script(r).hex()),
	])

def parse_sapling(r):
	nSpendsSapling = r.compact()
	vSpendsSapling = r.get(96 * nSpendsSapling)
	nOutputsSapling = r.compact()
	vOutputsSapling = r.get(756 * nOutputsSapling)
	if nSpendsSapling + nOutputsSapling > 0:
		valueBalanceSapling = r.uint64()
	if nSpendsSapling > 0:
		anchorSapling = r.get(32)
	vSpendProofsSapling = r.get(192 * nSpendsSapling)
	vSpendAuthSigsSapling = r.get(64 * nSpendsSapling)
	vOutputProofsSapling = r.get(192 * nOutputsSapling)
	if nSpendsSapling + nOutputsSapling > 0:
		bindingSigSapling = r.get(64)
	return dict([
		("nSpendsSapling", nSpendsSapling),
		("nOutputsSapling", nOutputsSapling),
	])

def parse_orchard(r):
	nActionsOrchard = r.compact()
	if nActionsOrchard == 0:
		return {"nActionsOrchard": nActionsOrchard}
	actions = [parse_action(r) for _ in range(nActionsOrchard)]
	flags = r.get(1)
	balance = r.sint64()
	anchor = r.get(32)
	sizeProof = r.compact()
	proof = r.get(sizeProof)
	return dict([
		("nActionsOrchard", nActionsOrchard),
		("actions", actions),
		("flags", flags.hex()),
		("balance", balance),
		("anchor", anchor.hex()),
		("sizeProof", sizeProof),
		("proof", proof[:20].hex() + "..."),
		("vSpendAuthSigsOrchard", [r.get(64).hex() for _ in range(nActionsOrchard)]),
		("bindingSigOrchard", r.get(64).hex()),
	])

def parse_action(r):
	return dict([
		("cv", r.get(32).hex()),
		("nf", r.get(32).hex()),
		("rk", r.get(32).hex()),
		("cmx", r.get(32).hex()),
		("epk", r.get(32).hex()),
		("C_enc", r.get(580).hex()[:20]+"..."),
		("C_out", r.get(80).hex()[:20]+"..."),
	])


if __name__ == "__main__":
	import sys

	try:
		tx_raw = sys.argv[1]
		if tx_raw == "load":
			tx_raw = input("tx: ").strip()
	except IndexError:
		try:
			with open("/home/agi/tx") as file:
				tx_raw = file.read()
			print("loading from file")
		except FileNotFoundError:
			tx_raw = input("tx: ").strip()
			print(tx_raw, len(set(tx_raw)))

	#tx_raw = "050000800a27a726b4d0d6c20000000001000000010000000000000000000000000000000000000000000000000000000000000000ffffffff03510101ffffffff0140be4025000000001976a9140facf8f06bc74944091207dca767d8f3af9fc78488ac000000"
	print("\n")


	data = bytes.fromhex(tx_raw)

	r = Reader(data)
	parsed = parse_tx(r)
	#parsed = [parse_action(r) for _ in range(r.compact())]
	import yaml
	print(yaml.dump(parsed, sort_keys=False))
	print()
	print("remaining data:", r.remaining())
