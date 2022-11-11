import json
import ref
from trezorlib.messages import ZcashOrchardInput
from py_trezor_orchard import OrchardInput


class TxInput:
    def __init__(self, **kwargs):
        for k, v in kwargs:
            setattr(self, k, v)


class OInput(TxInput):
    def as_trezor_input(self):
        return ZcashOrchardInput(**self.note)

    def has_witness():
        with open(f"/home/agi/code/ztrezor/notes/{self.cmx}.json", "r") as f:
            pos, path = json.load(f)
        return pos != 0

    def get_witness(self):
        with open(f"/home/agi/code/ztrezor/notes/{self.cmx}.json", "r") as f:
            pos, path = json.load(f)
        assert pos != 0
        path = list(map(bytes.fromhex, path))
        return (pos, path)

    def as_prover_input(self):
        return OrchardInput(self.as_trezor_input(), self.get_witness())

    def path(self):
        return f"m/32h/1h/{self.account}h"

    def value(self):
        return self.note["value"]


def TInput(TxInput):
    def path(self):
        x = self.inner.address_n
        H = 2 ** 31
        return f"m/{x[0]^H}h/{x[1]^H}h/{x[2]^H}h/{x[3]}/{x[4]}"

    def value(self):
        return self.inner.amount

    def as_trezor_input(self):
        return self.inner

    """
        TxInputType(
            address_n=parse_path("m/44h/1h/0h/0/0"),
            amount=amount,
            prev_hash=bytes.fromhex(txo["txid"]),
            prev_index=txo["output_no"],
            script_type={
                "76a914a579388225827d9f2fe9014add644487808c695d88ac": InputScriptType.SPENDADDRESS,
                #"scripthash": InputScriptType.PAYTOSCRIPTHASH,
            }[txo["script_hex"]],
        )
    """


def get_free_input(path, value=None):

    for txi in list(ref.get_every(TInput)) + list(ref.get_every(OInput)):
        if (
            txi.i.belongs_to is None and
            txi.i.path() == path and
            (value is None or txi.i.value() == value)
        ):
            return txi
    raise ValueError("Not enoght funding")
