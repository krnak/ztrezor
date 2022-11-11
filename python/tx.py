from common import *
from trezorlib.tools import parse_path
from trezorlib.messages import (
    OutputScriptType, ZcashOrchardOutput, TxOutputType, TxInputType
)
from trezorlib import zcash

from py_trezor_orchard import *
import api
import yaml
import time
from render import render_tx
import expected_messages
from tx_inputs import get_free_input, OInput, TInput
import ref


class Tx:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        setattr(self, "account", kwargs.get("account", 0))

    def as_ref(self):
        ref.get(self.name)

    def fund(self, resources, add_change=False):
        print(f"funding {self.name}")
        self.inputs = []
        for path, amount in self.funding:
            txi = get_free_input(path, amount)
            txi.i.belongs_to = self.name
            self.inputs.append(txi)
            self.as_ref().save()
        self.anchor = get_anchor()
        self.as_ref().save()

        balance = sum(f[1] for f in self.funding) - sum(txo.amount for txo in self.outputs)
        if add_change and balance > FEE:
            self.outputs.append(
                TxOutputType(
                    address_n=parse_path("m/44h/1h/0h/0/0"),
                    amount=balance - FEE,
                    script_type=OutputScriptType.PAYTOADDRESS,
                )
            )

        self.as_ref().save()

    def render(self):
        render_tx(self)

    def sign(self, force=False):
        if hasattr(self, "signatures") and not force:
            print("already signed")
            return
        print(f"signing {self.name}")

        protocol = zcash.sign_tx(
            get_client(),
            [txi.as_trezor_input() for txi in self.inputs],
            self.outputs,
            coin_name="Zcash Testnet",
            anchor=self.anchor,
            account=self.account,
            verbose=True,
        )
        self.shielding_seed = next(protocol)
        self.sighash = next(protocol)
        self.signatures, self.serialized_tx = next(protocol)

        #self.gen_expected()
        self.as_ref().save()

    def gen_expected(self):
        if not hasattr(self, "expect"):
            return
        if self.expect == "gen":
            print("generating expected messages")
            self.expect = list(expected_messages.gen(
                [],  #self.t_inputs,
                [],  #self.t_outputs,
                [],  #self.o_inputs,
                [],  #self.o_outputs,
                self.shielding_seed,
            ))
            self.as_ref().save()

    def prove(self, force=False):
        if hasattr(self, "orchard_serialized") and not force:
            print("already proven")
            return
        print(f"proving {self.name}")
        o_inputs = [txi for txi in self.inputs if isinstance(txi.i, OInput)]
        o_inputs = [txo for txo in self.outputs if isinstance(txo, ZcashOrchardOutput)]
        builder = TrezorBuilder(
            [x.as_prover_input() for x in o_inputs],
            [OrchardOutput(txo) for txo in o_outputs],
            self.anchor,
            fvk,
            self.shielding_seed,
        )

        bundle = builder.build()
        bundle.prepare(self.sighash)
        bundle.append_signatures(list(self.signatures[3].values()))
        print("proving")
        bundle.create_proof(pk())
        print("proving finished")
        bundle.finalize()
        self.orchard_serialized = bundle.serialized()
        #fvk2 = bytes.fromhex("4e2604c456d1c03f9889cd96e1bffc33b0b8033a60935c3768f710c66095b93bd9246f6bf20d5a01f234a5b1f8df86d53a1414a5887bdc961de3156a53fe2b106af481a091adf651ea47a59499ac5572beeedae394d8c3f3dddad54092c66336")
        for note, cmx in bundle.decrypt_outputs_with_fvk(fvk):
            ref.new(
                cmx.hex(),
                OInput(
                    note=note,
                    cmx=cmx.hex(),
                    account=self.account,
                    status="local"
                ),
            )

        with open("/home/agi/tx", "w") as f:
            print("save tx")
            f.write(self.serialized().hex())

        self.as_ref().save()

    def serialized(self):
        return self.serialized_tx[:-1] + self.orchard_serialized

    def save_to_tx(self):
        print(f"saving {self.name} to ~/tx")
        with open("/home/agi/tx", "w") as f:
            f.write(self.serialized().hex())

    def send(self, force=False):
        if hasattr(self, "txid") and not force:
            print("already sent")
        else:
            self.save_to_tx()
            self.txid = api.send_tx(tx_hex=self.serialized().hex())
            for utxn in self.o_inputs:
                spend_note(utxn[2])
            print(f"{self.name} sent as {self.txid}")
            self.as_ref().save()
        return self.txid

    def wait_for(self):
        while True:
            if api.is_tx_confirmed(self.txid):
                print("confirmed")
                break
            else:
                print("waiting for confirmation")
                time.sleep(30)
