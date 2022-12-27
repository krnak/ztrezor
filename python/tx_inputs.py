import json
from trezorlib.messages import ZcashOrchardInput
from py_trezor_orchard import OrchardInput


class TxInput:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def path(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError

    def as_trezor_input(self):
        raise NotImplementedError


class OInput(TxInput):
    def as_trezor_input(self):
        return ZcashOrchardInput(**self.note)

    def as_prover_input(self):
        return OrchardInput(self.as_trezor_input(), self.witness)

    def path(self):
        return f"m/32h/1h/{self.account}h"

    def value(self):
        return self.note["value"]


class TInput(TxInput):
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
