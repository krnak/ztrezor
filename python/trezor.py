import trezorlib
from trezorlib.client import get_default_client
from trezorlib import btc, messages, protobuf, zcash
from trezorlib.messages import ZcashSignatureType as SigType
from trezorlib.exceptions import TrezorFailure
from trezorlib.tools import parse_path
import json
from base64 import b64encode
from pprint import pprint

H = 1 <<31
ZEC = 10**8
FEE = int(0.0001 * ZEC)

def to_compact_size(n) -> None:
    assert 0 <= n <= 0xFFFF_FFFF
    if n < 253:
        return bytes([n])
    elif n <= 0xFFFF:
        return b"\xfd" + n.to_bytes(2, "little")
    elif n <= 0xFFFF_FFFF:
        return b"\xfe" + n.to_bytes(4, "little")
    else:
        return b"\xff" + n.to_bytes(8, "little")

proto = messages
inp1 = proto.TxInputType(
    # tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu
    address_n=parse_path("m/44h/1h/0h/0/0"),
    amount=1*ZEC,
    prev_hash=bytes.fromhex("d151621ce234da735a6e79de0b74829bab7ebf380cb7a2454b303dfde648e769"),
    prev_index=1,
)

real_inp = proto.TxInputType(
    # tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu
    address_n=parse_path("m/44h/1h/0h/0/0"),
    amount=1*ZEC,
    prev_hash=bytes.fromhex("9345936ea3b20371207d30d291effd6bf9b662dd3ecc41f0f3c9526e8e627b5a"),
    prev_index=0,
)

real_inp_2 = proto.TxInputType(
    # tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu
    address_n=parse_path("m/44h/1h/0h/0/0"),
    amount=1*ZEC,
    prev_hash=bytes.fromhex("184d1d11f2da3ff7c0687b95d7bb1a7bfa1814d7b9347cb0d49a77e92b447f35"),
    prev_index=0,
)

reg_inp = proto.TxInputType(
    # tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu
    address_n=parse_path("m/44h/1h/0h/0/0"),
    amount=6_25_000_000,
    prev_hash=bytes.fromhex("ba398aa2c303c2a6328ade3c5079ba3abd64dfdfcc183e4314c65702fed35800"),
    prev_index=0,
)

reg_out = proto.TxOutputType(
    address="tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu",
    amount=6_25_000_000 - FEE,
    script_type=proto.OutputScriptType.PAYTOADDRESS,
)
out1 = proto.TxOutputType(
    #address="tmJ1xYxP8XNTtCoDgvdmQPSrxh5qZJgy65Z",
    #address="t14oHp2v54vfmdgQ3v3SNuQga8JKHTNi2a1",
    #address="t1Lv2EguMkaZwvtFQW5pmbUsBw59KfTEhf4",
    address="tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu",
    amount=1*ZEC,
    script_type=proto.OutputScriptType.PAYTOADDRESS,
)
out_ua = proto.TxOutputType(
    address="utest1xt8k2akcdnncjfz8sfxkm49quc4w627skp3qpggkwp8c8ay3htftjf7tur9kftcw0w4vu4scwfg93ckfag84khy9k40yanl5k0qkanh9cyhddgws786qeqn37rtyf6rx4eflz09zk06",
    amount=1*ZEC - FEE,
    script_type=proto.OutputScriptType.PAYTOADDRESS,
)

out2 = proto.TxOutputType(
    address_n=parse_path("m/44h/133h/1h/0/0"),
    amount=1*ZEC,
    script_type=proto.OutputScriptType.PAYTOADDRESS,
)

out3 = proto.TxOutputType(
    address_n=parse_path("m/44h/133h/0h/0/0"),
    amount=1*ZEC,
    script_type=proto.OutputScriptType.PAYTOADDRESS,
)

client = get_default_client()
sin1 = messages.ZcashOrchardInput(
    recipient = b'\x16\x06\x18\xe7\xe5~\xb2\x9b\xfc\x11\x82\x10\x8a\x93:\xe1\xdb\xf8\xcc\xc1H\xd3\xcf\xa6\xc0\xa1Z\x04\xde\t\xe3\xc8\x84L\xd0{\xe8"3.\xaa)\x00',
    value = 99980000,
    rho = b'1V1\xb6\xb3e@$\x98\xb8\n$Q\xb3\xfe\x1e\x14H\x94\xa3\x0f\xab\xc8\xf0\xdf\x84\xe8\xfem\xaah\x1c',
    rseed = b'Aj\x02Gc\x8c\x0f~\xaf!SV#\r\xe1\xbb]i\xe9\xefIUv\xfbtjr\xf2}%\x97[',
    #cmx = b'\n\x19\xfcT\xd2\xfe\n\xf6@H\x94s1\x0fl\xb8\xf7=\xd8oD\x8b\xc1\x0b\xf5\x18u\xce\x14\x90N4'
)

# txid = f10749942b882272429f4301688b400b433f2a3b914205cb3e7635b5c538495c
sin2 = messages.ZcashOrchardInput(
    recipient = b'\x16\x06\x18\xe7\xe5~\xb2\x9b\xfc\x11\x82\x10\x8a\x93:\xe1\xdb\xf8\xcc\xc1H\xd3\xcf\xa6\xc0\xa1Z\x04\xde\t\xe3\xc8\x84L\xd0{\xe8"3.\xaa)\x00',
    value = 99980000,
    rho =  b'\x042\x91\xd5K\xc4D`!Ph"5@4\xa5\x02Z\x89F(\xe9*v\xb1\xb6\xebSf\xbb\xbb\x0c',
    rseed =  b'\x01\x9ck\xe9\xed\x02\xfb\xab\xcdQ\xb6\xab\xfe\xac\xa1\xd4\xafV\xb9\xae\xeb\xfa\xba\x0c\xff\xaf\xaf\xcd!\x00\x94\x1f',
)
# spend in 97ff06d3243407f9a187c8a0310ff75fd941cbe1b6a67fcf3dbeb935f474850b

anchor = bytes.fromhex("b6ed295d71902c0023a8695106dda23d98a679cf64269dcf2bc3060a6f4a4d07")
merkle_path = (
    30548,
    list(map(bytes.fromhex, [
        "8646890daed861a8f66a3966e884da1b1c8240bb47327a348fae9169eb820505",
        "d1ab2507c809c2713c000f525e9fbdcb06c958384e51b9cc7f792dde6c97f411",
        "18681f82320257f5a5cfc5c846fd4e88641d4ed7b87fcd5ec8e65e68e3ab0636",
        "2111fc397753e5fd50ec74816df27d6ada7ed2a9ac3816aab2573c8fac794204",
        "55cd8735904f69800ba500bf8af6fc70bfb2abb3d7ca1c75a1cce183b763f304",
        "873e4157f2c0f0c645e899360069fcc9d2ed9bc11bf59827af0230ed52edab18",
        "6e57cbad21bab804109f19479a88046b5c7f8da0d21e8217ac467801235c5220",
        "4e14563df191a2a65b4b37113b5230680555051b22d74a8e1f1d706f90f3133b",
        "a8773a2b01e9efd1011ea7d8d1071ad0a01c6c73e2fb6df802e307df17b4ac06",
        "a46523754a6d3fbc3226d6221dafca357d930e183297a0ba1cfa2db5d0500e1f",
        "b6fd291e9d6068bc24e99aefe49f8f29836ed1223deabc23871f1a1288f92403",
        "3ef9b30bae6122da1605bad6ec5d49b41d4d40caa96c1cf6302b66c5d2d10d39",
        "6fc552915a0d5bc5c0c0cdf29453edf081d9a2de396535e6084770c38dcff838",
        "9518d88883e466a41ca67d6b986739fb2f601d77bb957398ed899de70b2a9f08",
        "cd4871c1f545e7f5d844cc65fb00b8a162e316c3d1a435b00c435032b732c428",
        "63f8dbd10df936f1734973e0b3bd25f4ed440566c923085903f696bc6347ec0f",
        "2182163eac4061885a313568148dfae564e478066dcbe389a0ddb1ecb7f5dc34",
        "bd9dc0681918a3f3f9cd1f9e06aa1ad68927da63acc13b92a2578b2738a6d331",
        "ca2ced953b7fb95e3ba986333da9e69cd355223c929731094b6c2174c7638d2e",
        "55354b96b56f9e45aae1e0094d71ee248dabf668117778bdc3c19ca5331a4e1a",
        "7097b04c2aa045a0deffcaca41c5ac92e694466578f5909e72bb78d33310f705",
        "e81d6821ff813bd410867a3f22e8e5cb7ac5599a610af5c354eb392877362e01",
        "157de8567f7c4996b8c4fdc94938fd808c3b2a5ccb79d1a63858adaa9a6dd824",
        "fe1fce51cd6120c12c124695c4f98b275918fceae6eb209873ed73fe73775d0b",
        "1f91982912012669f74d0cfa1030ff37b152324e5b8346b3335a0aaeb63a0a2d",
        "5dec15f52af17da3931396183cbbbfbea7ed950714540aec06c645c754975522",
        "e8ae2ad91d463bab75ee941d33cc5817b613c63cda943a4c07f600591b088a25",
        "d53fdee371cef596766823f4a518a583b1158243afe89700f0da76da46d0060f",
        "15d2444cefe7914c9a61e829c730eceb216288fee825f6b3b6298f6f6b6bd62e",
        "4c57a617a0aa10ea7a83aa6b6b0ed685b6a3d9e5b8fd14f56cdc18021b12253f",
        "3fd4915c19bd831a7920be55d969b2ac23359e2559da77de2373f06ca014ba27",
        "87d063cd07ee4944222b7762840eb94c688bec743fa8bdf7715c8fe29f104c2a",
    ]))
)

def get_oinput(value):
    return ZcashOrchardInput(
        recipient = b'\x16\x06\x18\xe7\xe5~\xb2\x9b\xfc\x11\x82\x10\x8a\x93:\xe1\xdb\xf8\xcc\xc1H\xd3\xcf\xa6\xc0\xa1Z\x04\xde\t\xe3\xc8\x84L\xd0{\xe8"3.\xaa)\x00',
        value = value,
        rho = bytes([2]*32),
        rseed = bytes([2]*32),
    )

def get_change_sout(amount):
    return messages.ZcashOrchardOutput(
        amount = amount,
    )

sout1 = messages.ZcashOrchardOutput(
    amount = 1*ZEC,
)

sout2 = messages.ZcashOrchardOutput(
    address = "utest1xt8k2akcdnncjfz8sfxkm49quc4w627skp3qpggkwp8c8ay3htftjf7tur9kftcw0w4vu4scwfg93ckfag84khy9k40yanl5k0qkanh9cyhddgws786qeqn37rtyf6rx4eflz09zk06",
    amount = 1*ZEC,
    memo = "very important memo",
)

sout3 = messages.ZcashOrchardOutput(
    address = "utest1xt8k2akcdnncjfz8sfxkm49quc4w627skp3qpggkwp8c8ay3htftjf7tur9kftcw0w4vu4scwfg93ckfag84khy9k40yanl5k0qkanh9cyhddgws786qeqn37rtyf6rx4eflz09zk06",
    amount = 1*ZEC,
    #memo = "very important memo",
)

long_memo = messages.ZcashOrchardOutput(
    address = "utest1xt8k2akcdnncjfz8sfxkm49quc4w627skp3qpggkwp8c8ay3htftjf7tur9kftcw0w4vu4scwfg93ckfag84khy9k40yanl5k0qkanh9cyhddgws786qeqn37rtyf6rx4eflz09zk06",
    amount = 0*ZEC,
    memo = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Enim tortor at auctor urna nunc. Urna porttitor rhoncus dolor purus non enim praesent elementum facilisis. Amet purus gravida quis blandit turpis cursus in hac. Eu non diam phasellus vestibulum lorem sed risus. Pellentesque elit ullamcorper dignissim cras tincidunt. Egestas purus viverra accumsan in nisl nisi scelerisque eu ultrices. Morbi tincidunt ornare massa eget egestas purus.",
)

fvk = bytes.fromhex("d38d537a1195343afb128a58958f2cba8f6435488fa57e1a09c23451a07d7a14ca39d4b3d4163372065a1e54a4bc33d17f441f913ef91cda6e76c265fac32529d72fc9967f7751a5c8abc2b0b677879faef25871156faf6726ee79a7b4d5a00b")

config_2 = {
    "t_inputs": 4*[inp1],
    "t_outputs": [out1, out_ua],
    "o_inputs": [],
    "o_outputs": [sout2, sout3, long_memo],
}

config_3 = {
    "t_inputs": [real_inp],
    "t_outputs": [],
    "o_inputs": [],
    "o_outputs": [get_change_sout(1*ZEC - 2*FEE)],
}

config_4 = {
    "t_inputs": [real_inp_2],
    "t_outputs": [out1],
    "o_inputs": [],
    "o_outputs": [],
}

config_5 = {
    "t_inputs": [reg_inp],
    "t_outputs": [reg_out],
    "o_inputs": [],
    "o_outputs": [],
}

config_6 = {
    "t_inputs": [inp1],
    "t_outputs": [],
    "o_inputs": [],
    "o_outputs": [sout2],
}

config_7 = {
    "t_inputs": [],
    "t_outputs": [out1],
    "o_inputs": [sin2],
    "o_outputs": [],
}

config_8 = {
    "t_inputs": [],
    "t_outputs": [],
    "o_inputs": [],
    "o_outputs": [get_change_sout(0)],
}

config_8 = {
    "t_inputs": [],
    "t_outputs": [],
    "o_inputs": [sin1],
    "o_outputs": [get_change_sout(99980000)],
}

config = config_8

print("=== sign tx ===")
protocol = zcash.sign_tx(
    client,
    coin_name="Zcash Testnet",
    anchor=anchor,
    verbose=True,
    **config,
)

shielding_seed = next(protocol)
sighash = next(protocol)
print("sighash:", list(sighash))
signatures, serialized_tx = next(protocol)

if len(config["o_inputs"] + config["o_outputs"]) > 0 and input("=== prove (y/N):") == "y":
    import time
    from py_trezor_orchard import *

    inputs = [OrchardInput(txi, merkle_path) for txi in config["o_inputs"]]
    outputs = [OrchardOutput(txo) for txo in config["o_outputs"]]  #recipient

    builder = TrezorBuilder(
        inputs,
        outputs,
        anchor,
        fvk,
        shielding_seed,
    )
    bundle = builder.build()
    bundle.prepare(sighash)
    print(list(signatures[3].values()))
    # bundle.append_signatures(list(signatures[3].values()))

    """
    print("build the proving key")
    t1 = time.time()
    pk = ProvingKey.build()
    t2 = time.time()
    print("{:.2f} s".format(t2 - t1))

    print("create a proof")
    proof = bytes(prover.proof(witnesses, pk))
    t3 = time.time()
    print("{:.2f} s".format(t3 - t2))
    print("proof:", proof[:20], "...")

    with open("/home/agi/bundle", "wb") as file:
        file.write(serialized_bundle)
    """

print("=======")
print("saving to ~/tx")
with open("/home/agi/tx", "w") as file:
    file.write(serialized_tx.hex())
print("=======")
