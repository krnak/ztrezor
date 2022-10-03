H = 1 << 31
ZEC = 10**8
FEE = int(0.0001 * ZEC)
BASE = int(0.01 * ZEC)

fvk = bytes.fromhex("d38d537a1195343afb128a58958f2cba8f6435488fa57e1a09c23451a07d7a14ca39d4b3d4163372065a1e54a4bc33d17f441f913ef91cda6e76c265fac32529d72fc9967f7751a5c8abc2b0b677879faef25871156faf6726ee79a7b4d5a00b")

from py_trezor_orchard import ProvingKey, OrchardInput
from trezorlib.messages import ZcashOrchardInput
import json
import os


PK = None


def pk():
    global PK
    if PK is None:
        print("building proving key")
        PK = ProvingKey.build()
        print("proving key built")
    return PK


def load_note(cmx):
    with open(f"/home/agi/code/ztrezor/notes/{cmx}.json", "r") as f:
        note = json.load(f)
    with open(f"/home/agi/code/ztrezor/witnesses/{cmx}.json", "r") as f:
        pos, path = json.load(f)

    path = list(map(bytes.fromhex, path))
    input = ZcashOrchardInput(
        recipient=bytes(note["recipient"]),
        value=note["value"],
        rho=bytes(note["rho"]),
        rseed=bytes(note["rseed"]),
    )
    return input, OrchardInput(input, (pos, path)), cmx

def spend_note(cmx):
    print(f"spend note {cmx}")
    os.rename(f"/home/agi/code/ztrezor/notes/{cmx}.json", f"/home/agi/code/ztrezor/spent_notes/{cmx}.json")
    os.remove(f"/home/agi/code/ztrezor/witnesses/{cmx}.json")
