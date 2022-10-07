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


class Tx:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def load(name):
        print(f"loading tx {name}")
        with open(f"/home/agi/code/ztrezor/txs/{name}.yaml", "r") as f:
            return yaml.load(f.read(), Loader=yaml.Loader)

    def save(self):
        print(f"saving tx {self.name}")
        with open(f"/home/agi/code/ztrezor/txs/{self.name}.yaml", "w") as f:
            f.write(yaml.dump(self))

    def fund(self, resources, add_change=False):
        print(f"funding {self.name}")
        for k in self.funding:
            if len(resources[k]) < self.funding.count(k):
                raise ValueError("not enough resources")

        inputs = [resources[txi].pop() for txi in self.funding]
        self.t_inputs = [txi for txi in inputs if isinstance(txi, TxInputType)]
        self.o_inputs = [txi for txi in inputs if isinstance(txi, tuple)]
        self.t_outputs = [txo for txo in self.outputs if isinstance(txo, TxOutputType)]
        self.o_outputs = [txo for txo in self.outputs if isinstance(txo, ZcashOrchardOutput)]
        self.anchor = get_anchor()

        balance = sum(f[1] for f in self.funding) - sum(txo.amount for txo in self.t_outputs + self.o_outputs)
        if add_change and balance > FEE:
            self.t_outputs.append(
                TxOutputType(
                    address_n=parse_path("m/44h/1h/0h/0/0"),
                    amount=balance - FEE,
                    script_type=OutputScriptType.PAYTOADDRESS,
                )
            )

        self.save()

    def render(self):
        render_tx(self)

    def sign(self, force=False):
        if hasattr(self, "signatures") and not force:
            print("already signed")
            return
        print(f"signing {self.name}")

        protocol = zcash.sign_tx(
            get_client(),
            self.t_inputs,
            self.t_outputs,
            [x[0] for x in self.o_inputs],
            self.o_outputs,
            coin_name="Zcash Testnet",
            anchor=self.anchor,
            account=getattr(self, "account", default=0),
            verbose=True,
        )
        self.shielding_seed = next(protocol)
        self.sighash = next(protocol)
        self.signatures, self.serialized_tx = next(protocol)

        self.save()

    def prove(self, force=False):
        if hasattr(self, "orchard_serialized") and not force:
            print("already proven")
            return
        print(f"proving {self.name}")
        builder = TrezorBuilder(
            [OrchardInput(x[0], x[1]) for x in self.o_inputs],
            [OrchardOutput(txo) for txo in self.o_outputs],
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

        for note, cmx in bundle.decrypt_outputs_with_fvk(fvk):
            create_note(cmx.hex(), note, getattr(self, "account", default=0))

        with open("/home/agi/tx", "w") as f:
            print("save tx")
            f.write(self.serialized().hex())

        self.save()

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
            self.save()
        return self.txid

    def wait_for(self):
        while True:
            if api.is_tx_confirmed(self.txid):
                print("confirmed")
                break
            else:
                print("waiting for confirmation")
                time.sleep(30)
