from tx_inputs import OInput, TInput
from trezorlib.messages import TxOutputType, ZcashOrchardOutput

H = 1 << 31


def show_path(path):
    hard = [((H, "h") if i >= H else (0, "")) for i in path]
    return "m/" + "/".join(str(i ^ h[0]) + h[1] for i, h in zip(path, hard))


def render_o_input(i, note, cmx):
    return f"""
    # note { cmx }
    inp_{i} = ZcashOrchardInput(
        recipient=bytes.fromhex(\"{note.recipient.hex()}\"),
        value={note.value},
        rho=bytes.fromhex(\"{note.rho.hex()}\"),
        rseed=bytes.fromhex(\"{note.rseed.hex()}\"),
    )
    """

def none_or_string(x):
    if x is None:
        return "None"
    if isinstance(x, str):
        return f'"{x}"'

def render_o_output(i, txo):
    return f"""
    out_{i} = ZcashOrchardOutput(
        address={none_or_string(txo.address)},
        amount={txo.amount},
        memo={none_or_string(txo.memo)},
    )"""

def render_t_input(i, txi):
    return f"""
    inp_{i} = TxInputType(
        address_n=parse_path(\"{show_path(txi.address_n)}\"),
        amount={txi.amount},
        prev_hash=bytes.fromhex(\"{txi.prev_hash.hex()}\"),
        prev_index={txi.prev_index},
    )"""


def render_t_output(i, txo):
    if txo.address:
        address = f"address=\"{txo.address}\""
    else:
        address = f"address_n=parse_path(\"{show_path(txo.address_n)}\")"
    return f"""
    out_{i} = TxOutputType(
        {address},
        amount={txo.amount},
        script_type=OutputScriptType.PAYTOADDRESS,
    )"""


def render_tx(tx):
    print(f"render {tx.name}")
    f = open(f"/home/agi/gh/jarys/ztrezor/rendered/{tx.name}.py", "w")
    f.write(f"def test_{tx.name}(client: Client) -> None:")
    for i, txi in enumerate(tx.inputs):
        if isinstance(txi, TInput):
            f.write(render_t_input(i, txi.as_trezor_input()))
        if isinstance(txi, OInput):
            f.write(render_o_input(i, txi.as_trezor_input(), txi.cmx))
    for i, txo in enumerate(tx.outputs):
        if isinstance(txo, TxOutputType):
            f.write(render_t_output(i, txo))
        if isinstance(txo, ZcashOrchardOutput):
            f.write(render_o_output(i, txo))
    f.write(f"""
    anchor = bytes.fromhex(\"{tx.anchor.hex()}\")\n""")
    if not tx.raises:
        f.write(f"""\
    expected_shielding_seed = bytes.fromhex(\"{tx.shielding_seed.hex()}\")
    expected_sighash = bytes.fromhex(\"{tx.sighash.hex()}\")
    expected_serialized_tx = bytes.fromhex(\"{tx.serialized_tx.hex()}\")\n""")
    
    expected_messages = "".join(f"""
                {x}""" for x in tx.expect)
    if expected_messages:
        expected_messages += "\n            "

    f.write(f"""
    with client:
        client.set_expected_responses(
            [{expected_messages}]
        )\n\n""")
    if not tx.raises:
        f.write(f"""\
        protocol = zcash.sign_tx(
            client,
            inputs=[{ ", ".join(f"inp_{i}" for i in range(len(tx.inputs))) }],
            outputs=[{ ", ".join(f"out_{i}" for i in range(len(tx.outputs))) }],
            coin_name=\"Zcash Testnet\",
            z_address_n=parse_path("{show_path(tx.z_address_n)}"),
            anchor=anchor,
        )
        """)
        t_sigs = "".join(f"""
                bytes.fromhex(\"{sig.hex()}\"),""" for sig in tx.signatures[0])
        if t_sigs:
            t_sigs += "\n            "
        o_sigs = "".join(f"""
                {k}: bytes.fromhex(\"{sig.hex()}\"),""" for k, sig in tx.signatures[3].items())
        if o_sigs:
            o_sigs += "\n            "
        f.write(f"""
        shielding_seed = next(protocol)
        assert shielding_seed == expected_shielding_seed
        sighash = next(protocol)
        assert sighash == expected_sighash
        signatures, serialized_tx = next(protocol)
        assert serialized_tx == expected_serialized_tx
        assert signatures == {{
            ZcashSignatureType.TRANSPARENT: [{t_sigs}],
            ZcashSignatureType.ORCHARD_SPEND_AUTH: {{{o_sigs}}},
        }}

        # Accepted by network as {tx.txid}\n""")
    else:
        f.write(f"""\
        with pytest.raises(TrezorFailure, match="{ tx.exception }"):
            protocol = zcash.sign_tx(
                client,
                inputs=[{ ", ".join(f"inp_{i}" for i in range(len(tx.inputs))) }],
                outputs=[{ ", ".join(f"out_{i}" for i in range(len(tx.outputs))) }],
                coin_name=\"Zcash Testnet\",
                z_address_n=parse_path("{show_path(tx.z_address_n)}"),
                anchor=anchor,
            )
            next(protocol)  # shielding seed
            next(protocol)  # sighash
            next(protocol)  # serialized_tx and signatures
        """)
    f.close()
