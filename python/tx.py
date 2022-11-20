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
from tx_inputs import OInput, TInput


class Tx:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        setattr(self, "account", kwargs.get("account", 0))

    def fund(self, resources, add_change=False):
        print(f"funding { self.name }")

        # improvised solution
        anchors = set(txis[0].anchor for txis in resources.values() if isinstance(txis[0], OInput))
        print(anchors)
        assert len(anchors) == 1
        self.anchor = anchors.pop()

        self.inputs = []
        for input_params in self.funding:
            if input_params not in resources:
                raise ValueError(f"missing inout of type { input_params }")
            self.inputs.append(resources[input_params].pop())

        balance = sum(f[1] for f in self.funding) - sum(txo.amount for txo in self.outputs)
        if add_change and balance > FEE:
            self.outputs.append(
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
            [txi.as_trezor_input() for txi in self.inputs],
            self.outputs,
            coin_name="Zcash Testnet",
            anchor=self.anchor,
            account=self.account,
        )
        self.shielding_seed = next(protocol)
        self.sighash = next(protocol)
        self.signatures, self.serialized_tx = next(protocol)

        #self.gen_expected()
        self.save()

    def gen_expected(self):
        if not hasattr(self, "expect"):
            return
        if self.expect == "gen":
            print("generating expected messages")
            self.expect = list(expected_messages.gen(
                [],  # self.t_inputs,
                [],  # self.t_outputs,
                [],  # self.o_inputs,
                [],  # self.o_outputs,
                self.shielding_seed,
            ))
            self.save()

    def prove(self, force=False):
        if hasattr(self, "orchard_serialized") and not force:
            print("already proven")
            return
        print(f"proving {self.name}")
        self.sighash = 32 * b"\x00"
        self.signatures = {0: {}, 3: {}}
        builder = TrezorBuilder(
            [txi.as_prover_input()
                for txi in self.inputs
                if isinstance(txi, OInput)
            ],
            [OrchardOutput(txo)
                for txo in self.outputs
                if isinstance(txo, ZcashOrchardOutput)
            ],
            self.anchor,
            fvk,
            32*b"\x00",
            #self.zcash_shielding_seed,
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

        self.save_to_tx()
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

    def save(self):
        with open(f"/home/agi/code/ztrezor/txs/{ self.name }.yaml", "w") as f:
            yaml.dump(self, f)

    def load(name):
        with open(f"/home/agi/code/ztrezor/txs/{ name }.yaml") as f:
            return yaml.load(f, Loader=yaml.Loader)
