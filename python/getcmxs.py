import subprocess
import json
from ztx import parse_tx, Reader


def get(command, parse_json=True):
    # print(command)
    result = subprocess.run(['zcash-cli', *command], stdout=subprocess.PIPE)
    result = result.stdout
    # return result.stdout.decode("utf-8")
    if parse_json:
        try:
            result = json.loads(result)
        except json.decoder.JSONDecodeError:
            print(result.stdout)
            exit(0)
    return result


def sync():
    with open("/home/agi/cmxs.testnet.meta") as file:
        meta = json.load(file)

    info = get(["getblockchaininfo"])
    scan_start = max(
        meta["last_block"] + 1,
        info["upgrades"]["c2d6d0b4"]["activationheight"],
    )
    scan_end = info["blocks"]
    print(f"scanning of range {scan_start}..{scan_end}")

    cmx_n = 0
    new_cmxs = []
    with open("/home/agi/cmxs.testnet", "ab") as file:
        for i in range(scan_start, scan_end + 1):
            if i % 10 == 0:
                print("block", i)
            block = get(["getblock", str(i)])
            for txid in block["tx"]:
                tx_hex = get(["getrawtransaction", txid], False)
                tx_raw = bytes.fromhex(tx_hex.decode())
                if tx_raw[0] == 4:
                    continue
                tx = parse_tx(Reader(tx_raw))
                for j, action in enumerate(tx["orchard"].get("actions", [])):
                    cmx = action["cmx"]
                    new_cmxs.append(cmx)
                    file.write(bytes.fromhex(cmx))
                    cmx_n += 1
                    if cmx_n % 100 == 0:
                        print("cmx_n:", cmx_n)
                    # print(f"block {i} tx {txid[:8]} action {j} cmx: {cmx}")

    with open("/home/agi/cmxs.testnet.meta", "w") as file:
        meta = json.dump({"last_block": scan_end}, file)

    return new_cmxs


if __name__ == "__main__":
    sync()
