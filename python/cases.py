from common import *
from trezorlib.tools import parse_path
from trezorlib.messages import (
    OutputScriptType, ZcashOrchardOutput, TxOutputType
)
from tx import Tx

CASES = [
    # t2z
    Tx(
        name="t2z",
        funding=[("m/44h/1h/0h/0/0", BASE)],
        outputs=[ZcashOrchardOutput(amount=BASE - FEE)],
        expect=None,
    ),
    Tx(
        name="z2z",
        funding=[("m/32h/1h/0h", BASE)],
        outputs=[ZcashOrchardOutput(amount=BASE - FEE)],
        expect=None,
    ),
    Tx(
        name="z2t",
        outputs=[
            TxOutputType(
                address_n=parse_path("m/44h/1h/0h/0/0"),
                amount=BASE - FEE,
                script_type=OutputScriptType.PAYTOADDRESS,
            )
        ],
        funding=[("m/32h/1h/0h", BASE)],
        expect=None,
    ),
    # long mem
    # many inputs
    # dust inputs
    # many outputs
    # too many action
    # self forward
    # to big fee
]

ADDRESS = [
    "utest1gu6rg6hse8v0pd7mhgfn80v5vvdhuwn30wztyrczxsyj46ngpp2ryw36az6vlmlle8xns5k6pdlkgycr27naa2hpn3wspuvsxv0yzz62",
    "utest1rgn5dkcq9vcf3vr7el74m2p2lslfw9ndn9dqm44ram756f544fndvd82ecv37gkxuum8mr8yrtjlnjwumgn48qrqlhch4znnqselfr5j",
    "utest15w5alyhzu2l4k9umc3zxkv4x5mdg3ass97pu7n29arwaxrgc2r7xct3d3j0w0p26mvqxgrku2203xvp9nkwvfgdf9cxmyxlkm5n5cclt",
    "utest1ms4aqpys9vpqdh52cq9stgyuam0wgw7whjtp3xshly5xpnp0070jlvh8dh280vudhg845psrdsx6zv8yvkju9v62cqtg8x8xcv2dxp4a",
    "utest1lqcxy5sleh0dsdgxefj3jpehkwugxdvmfmemswa0xns3thhq5f2tuydl649utcktpydlttydnamprk3ddm22wszmcpzt608jws9s02nu",
    "utest1jdqlx5evfxs65f05kgjdk9gtselavgredtg2kd4pzyf435hwfv250gel6k5hqhsx6rjsl2fauv8s4as7hy9fm2g7kd5vte834qyyupw9",
    "utest19d9xjz0wu73u6h245c3v6j0wv3657akg0qvj0x45cars0dgl7vzdwa3dkm5zhsvgsas4z3wd79ua0ayl0nlcsfgpn0zawmqnlualld52",
    "utest17rr4l9yjvk6le0aqa4vt0aauudhe07tvslhuvhmcds2jnklzx02hn0uw0xegs6ekgnu0ulyeqs6shjzepl2jemuesxpllmuj2gezg4zv",
    "utest1kc3jtr400mlzpqa0sp3w8v5nnljyq6g0lw6hw30jx0ym3vkswsgyus2ujlnntvls2uyulqstj4wf8ahxce2uahq06hf8jla3qymdvxur",
    "utest1rusrelt7xyc62chav9r6cv5nnxp63eemm3rm0qpaqs578hkjpr9rgyvuyjm3nxpcjfx8a7dquyt2shkw5xl23m523t3cgkt7wsd9mue3",
]

CASES_2 = [
    Tx(
        name="long_memo",
        funding=[("m/32h/1h/0h", BASE)],
        outputs=[ZcashOrchardOutput(
            address="utest1xt8k2akcdnncjfz8sfxkm49quc4w627skp3qpggkwp8c8ay3htftjf7tur9kftcw0w4vu4scwfg93ckfag84khy9k40yanl5k0qkanh9cyhddgws786qeqn37rtyf6rx4eflz09zk06",
            amount=BASE - FEE,
            memo="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Enim tortor at auctor urna nunc. Urna porttitor rhoncus dolor purus non enim praesent elementum facilisis. Amet purus gravida quis blandit turpis cursus in hac. Eu non diam phasellus vestibulum lorem sed risus. Pellentesque elit ullamcorper dignissim cras tincidunt. Egestas purus viverra accumsan in nisl nisi scelerisque eu ultrices. Morbi tincidunt ornare massa eget egestas purus.",
        )],
        expect=None,
    ),
    Tx(
        name="dust_inputs",
        funding=[12*("m/32h/1h/0h", BASE)],
        outputs=[
            ZcashOrchardOutput(
                address=ADDRESS[9],
                amount=12*BASE - FEE,
                memo="dust inputs",
            )
        ],
        expect=None,
    ),
    Tx(
        name="big_bundle",
        funding=[8*("m/32h/1h/0h", BASE)],
        outputs=[
            ZcashOrchardOutput(
                address=ADDRESS[i],
                amount=BASE,
            )
            for i in range(8)
        ],
        expect=None,
    )
    # too many actions
    Tx(
        name="too_large_fee",
        funding=[("m/32h/1h/0h", int(0.5 * ZEC))],
        outputs=[ZcashOrchardOutput(
            address="utest1xt8k2akcdnncjfz8sfxkm49quc4w627skp3qpggkwp8c8ay3htftjf7tur9kftcw0w4vu4scwfg93ckfag84khy9k40yanl5k0qkanh9cyhddgws786qeqn37rtyf6rx4eflz09zk06",
            amount=int(0.1 * ZEC),
            memo="too large fee",
        )],
        expect=None,
    ),
    Tx(
        name="send_to_account_2",
        funding=[("m/32h/1h/0h", BASE)],
        outputs=[ZcashOrchardOutput(
            address="utest1d5kpwc69vplme7sae0rjmc88599xxy03767yzpplessv72p3pf3e023lkhs8zxdxw3slvnj4xaf0u3sqp9qe7qf0vq0fcc2jpcr87cks",
            amount=BASE - FEE,
            memo="from acount 0 to acount 2",
        )],
        expect=None,
    ),
    Tx(
        name="send_from_account_2",
        funding=[("m/32h/1h/2h", BASE)],
        outputs=[ZcashOrchardOutput(
            address=ADDRESS[0],
            amount=BASE - FEE,
            memo="from acount 2 to account 0",
        )],
        expect=None,
        account=2,
    )
]
