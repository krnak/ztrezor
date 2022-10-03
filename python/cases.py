from common import *
from trezorlib.tools import parse_path
from trezorlib.messages import (
    OutputScriptType, ZcashOrchardOutput, TxOutputType, TxInputType
)
from trezorlib import zcash

from py_trezor_orchard import *
import api

class TestCase:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def send(self, client, sources, anchor):
        print(f"=== SENDING TEST CASE {self.name} ===")
        t_inputs = [sources[txi].pop() for txi in self.t_inputs]
        o_inputs = [sources[txi].pop() for txi in self.o_inputs]
        protocol = zcash.sign_tx(
            client,
            t_inputs,
            self.t_outputs,
            [x[0] for x in o_inputs],
            self.o_outputs,
            coin_name="Zcash Testnet",
            anchor=anchor,
            verbose=True,
        )
        shielding_seed = next(protocol)
        sighash = next(protocol)
        signatures, serialized_tx = next(protocol)

        builder = TrezorBuilder(
            [x[1] for x in o_inputs],
            [OrchardOutput(txo) for txo in self.o_outputs],
            anchor,
            fvk,
            shielding_seed,
        )

        bundle = builder.build()
        bundle.prepare(sighash)
        bundle.append_signatures(list(signatures[3].values()))
        print("proving")
        bundle.create_proof(pk())
        print("proving finished")
        bundle.finalize()

        tx = serialized_tx[:-1] + bytes(bundle.serialized())
        with open("/home/agi/tx", "w") as f:
            print("save tx")
            f.write(tx.hex())
        txid = api.send_tx(tx_hex=tx.hex())
        for utxn in o_inputs:
            spend_note(utxn[2])
        print(f"=== finished as {txid} ===")
        return txid

"""
    TestCase(
        name="",
        t_inputs=[],
        t_outputs=[],
        o_inputs=[],
        o_outputs=[],
        expect=None,
    ),
"""

CASES = [
    # t2z
    TestCase(
        name="t2z",
        t_inputs=[("m/44h/1h/0h/0/0", BASE)],
        t_outputs=[],
        o_inputs=[],
        o_outputs=[ZcashOrchardOutput(amount=BASE - FEE)],
        expect=None,
    ),
    TestCase(
        name="z2z",
        t_inputs=[],
        t_outputs=[],
        o_inputs=[("m/32h/1h/0h", BASE)],
        o_outputs=[ZcashOrchardOutput(amount=BASE - FEE)],
        expect=None,
    ),
    TestCase(
        name="z2t",
        t_inputs=[],
        t_outputs=[
            TxOutputType(
                address_n=parse_path("m/44h/1h/0h/0/0"),
                amount=BASE - FEE,
                script_type=OutputScriptType.PAYTOADDRESS,
            )
        ],
        o_inputs=[("m/32h/1h/0h", BASE)],
        o_outputs=[],
        expect=None,
    ),
    # long memo
    # many inputs
    # dust inputs
    # many outputs
    # too many action
    # self forward
    # to big fee
]


def required_utxos():
    for case in CASES:
        for path, amount in case.t_inputs:
            yield TxOutputType(
                address_n=parse_path(path),
                amount=amount,
                script_type=OutputScriptType.PAYTOADDRESS,
            )


def required_utxns():
    for case in CASES:
        for path, amount in case.o_inputs:
            yield ZcashOrchardOutput(
                address_n=parse_path(path),
                amount=amount,
            )
