H = 1 << 31


def show_path(path):
    hard = [((H, "h") if i >= H else (0, "")) for i in path]
    return "m/" + "/".join(str(i ^ h[0]) + h[1] for i, h in zip(path, hard))


def render_o_input(i, note, cmx):
    return f"""
    # note {cmx}
    o_inp_{i} = ZcashOrchardInput(
        recipient=bytes.fromhex(\"{note.recipient.hex()}\"),
        value={note.value},
        rho=bytes.fromhex(\"{note.rho.hex()}\"),
        rseed=bytes.fromhex(\"{note.rseed.hex()}\"),
    )
    """


def render_o_output(i, txo):
    return f"""
    o_out_{i} = ZcashOrchardOutput(
        address={txo.address},
        amount={txo.amount},
        memo={txo.memo},
    )"""

def render_t_input(i, txi):
    return f"""
    t_inp_{i} = TxInputType(
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
    t_out_{i} = TxOutputType(
        {address},
        amount={txo.amount},
        script_type=OutputScriptType.PAYTOADDRESS,
    )"""


def render_tx(tx):
    print(f"render {tx.name}")
    f = open(f"/home/agi/code/ztrezor/rendered/{tx.name}.py", "w")
    f.write(f"def test_{tx.name}(client: Client) -> None:")
    for i, txi in enumerate(tx.t_inputs):
        f.write(render_t_input(i, txi))
    for i, txo in enumerate(tx.t_outputs):
        f.write(render_t_output(i, txo))
    for i, (txi, _, cmx) in enumerate(tx.o_inputs):
        f.write(render_o_input(i, txi, cmx))
    for i, txo in enumerate(tx.o_outputs):
        f.write(render_o_output(i, txo))
    f.write(f"""
    anchor = bytes.fromhex(\"{tx.anchor.hex()}\")
    expected_shielding_seed = bytes.fromhex(\"{tx.shielding_seed.hex()}\")
    expected_sighash = bytes.fromhex(\"{tx.sighash.hex()}\")
    expected_serialized_tx = bytes.fromhex(\"{tx.serialized_tx.hex()}\")
    """)
    expected_messages = "".join(f"""
                {x}""" for x in tx.expected)
    if expected_messages:
        expected_messages += "\n            "

    f.write(f"""
    with client:
        client.set_expected_responses(
            [{expected_messages}]
        )

        protocol = zcash.sign_tx(
            client,""")
    for to in ["t", "o"]:
        for io, inout in [("inp", "input"), ("out", "output")]:
            cont = ", ".join(f"{to}_{io}_{i}" for i in range(len(getattr(tx, f"{to}_{inout}s"))))
            f.write(f"\n            {to}_{inout}s=[{cont}],")
    t_sigs = "".join(f"""
                bytes.fromhex(\"{sig.hex()}\"),""" for sig in tx.signatures[0])
    if t_sigs:
        t_sigs += "\n            "
    o_sigs = "".join(f"""
                {k}: bytes.fromhex(\"{sig.hex()}\"),""" for k, sig in tx.signatures[3].items())
    if o_sigs:
        o_sigs += "\n            "
    f.write(f"""
            anchor=anchor,
            coin_name=\"Zcash Testnet\",
        )

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

        # Accepted by network as {tx.txid}
        # link: https://sochain.com/tx/ZECTEST/{tx.txid}\n\n""")
    f.close()
