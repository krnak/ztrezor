import trezorlib
from trezorlib.client import get_default_client
from trezorlib import btc, messages, protobuf, zcash
from trezorlib.exceptions import TrezorFailure
from trezorlib.tools import parse_path
import json
from base64 import b64encode


def encode_memo(memo):
	if memo is None:
		return None
	if type(memo) is bytes:
		assert len(memo) == 512
		assert memo[0] > 0XF5
		return memo
	if type(memo) is str:
		memo = memo.encode("utf-8")
		memo += b"\x00"*(512 - len(memo))
		return memo

H = 1 <<31
ZEC = 10**8
FEE = int(0.0001 * ZEC)

proto = messages
inp1 = proto.TxInputType(
	# tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu
	address_n=parse_path("m/44h/1h/0h/0/0"),
	amount=1*ZEC - FEE,
	prev_hash=bytes.fromhex("51b6fe450432ecf66cae40f2932a5a3d882e9855743e68f8c197b79f5d1382af"),
	prev_index=0,
)

out1 = proto.TxOutputType(
	#address="tmJ1xYxP8XNTtCoDgvdmQPSrxh5qZJgy65Z",
	#address="t14oHp2v54vfmdgQ3v3SNuQga8JKHTNi2a1",
	#address="t1Lv2EguMkaZwvtFQW5pmbUsBw59KfTEhf4",
	address="tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu",
	amount=1*ZEC - FEE,
	script_type=proto.OutputScriptType.PAYTOADDRESS,
)

out2 = proto.TxOutputType(
	address_n=parse_path("m/44h/133h/1h/0/0"),
	amount=1*ZEC,
	script_type=proto.OutputScriptType.PAYTOADDRESS,
)

out3 = proto.TxOutputType(
	address_n=parse_path("m/44h/133h/0h/0/0"),
	amount=1*ZEC,
	script_type=proto.OutputScriptType.PAYTOADDRESS,
)

client = get_default_client()

def get_note(value):
	note = bytearray(83*b"\x00")
	note[43:51] = value.to_bytes(8, byteorder='little')
	return bytes(note)

sin1 = {
	#amount: 100000000,
	"address_n": [32|H, 133|H, 0|H],
	"note": get_note(7*ZEC)
}

sout1 = {
	"decryptable": True,
	"ovk_address_n": [32|H, 133|H, 0|H],
	"address_n": [32|H, 133|H, 0|H],
	"amount": 1*ZEC - FEE,
	"memo": b"unseen memo ahoj",
}

sout2 = {
	"decryptable": False,
	"address": "u1qylzskzykhk5l5vk6zlyqqruvskzv74hk20lmrllzy3vdz6pvny5t9zwlrm86ukw77y5pu8uep2m33s7sc7gn6aq0jm9neg5tsektyn9",
	"amount": 1*ZEC,
	"memo": encode_memo("very important memo"),
}

sout3 = {
	"decryptable": True,
	"ovk_address_n": [32|H, 133|H, 1|H],
	"address_n": [32|H, 133|H, 1|H],
	"amount": 1*ZEC,
	#"memo": b"",
}

t_signatures, o_signatures, serialized_tx, seed = zcash.sign_tx(
	client,
	[], #[sinp1],
	[sout1], #[sout1, sout2], #[sout1, sout2, sout3],
	[inp1],
	[], #[out1], #[out1, out2, out3],
	"Zcash Testnet"
)
print("t_signatures:", t_signatures)
print("o_signatures:", o_signatures)
print("serialized_tx:", (serialized_tx+b"\x00").hex())
print("serialized_tx_b64:", b64encode(serialized_tx+b"\x00"))
print("seed:", seed)

if input("prove (y/N):") == "y":
	sighash = eval(input("sighash:"))
	assert type(sighash) == bytes
	assert len(sighash) == 32

	from pyorchard import *
	print("prepare a builder.")
	anchor = bytes.fromhex("ae2935f1dfd8a24aed7c70df7de3a668eb7a49b1319880dde2bbd9031ae5d82f")
	builder = Builder(anchor)
	output = Output(
		None,
		Address.from_bytes(
			bytes.fromhex("8ff3386971cb64b8e7789908dd8ebd7de92a68e586a34db8fea999efd2016fae76750afae7ee941646bcb9")
		),
		sout1["amount"],
		None
	)
	builder.add_output(output)
	rng = Random.from_seed(seed)
	print("build a bundle")
	bundle = builder.build(rng)
	print("build the proving key")
	pk = ProvingKey.build()
	print("prepare the bundle")
	bundle.prepare(rng, sighash)
	print("create a proof")
	bundle.create_proof(pk, rng)
	print("finalize")
	bundle.finalize()
	orchard_bundle_serialized = bytes(bundle.serialized())
	print("=== serialized tx (hex) ===")
	print((serialized_tx + orchard_bundle_serialized).hex())
	print("=== serialized tx (base64) ===")
	print(b64encode((serialized_tx + orchard_bundle_serialized)))
