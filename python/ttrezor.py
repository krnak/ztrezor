import trezorlib
from trezorlib.client import get_default_client
from trezorlib import btc, messages, protobuf
from trezorlib.exceptions import TrezorFailure
from trezorlib.tools import parse_path
import json

H = 1 <<31
ZEC = 10**8
FEE = int(0.0001 * ZEC)

proto = messages
inp1 = proto.TxInputType(
	# tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu
	address_n=parse_path("m/44h/133h/0h/0/0"),
	amount=3*ZEC,
	prev_hash=32*b"\xee",
	prev_index=0,
)

out1 = proto.TxOutputType(
	#address="tmJ1xYxP8XNTtCoDgvdmQPSrxh5qZJgy65Z",
	#address="t14oHp2v54vfmdgQ3v3SNuQga8JKHTNi2a1",
	address="t1Lv2EguMkaZwvtFQW5pmbUsBw59KfTEhf4",
	amount=1*ZEC,
	script_type=proto.OutputScriptType.PAYTOADDRESS,
)

out2 = proto.TxOutputType(
	address_n=parse_path("m/44h/133h/1h/0/0"),
	amount=1*ZEC,
	script_type=proto.OutputScriptType.PAYTOADDRESS,
)

out3 = proto.TxOutputType(
	address_n=parse_path("m/44h/133h/0h/0/0"),
	amount=1*ZEC - FEE,
	script_type=proto.OutputScriptType.PAYTOADDRESS,
)

TXHASH_aaf51e = bytes.fromhex(
    "aaf51e4606c264e47e5c42c958fe4cf1539c5172684721e38e69f4ef634d75dc"
)
TXHASH_e38206 = bytes.fromhex(
    "e3820602226974b1dd87b7113cc8aea8c63e5ae29293991e7bfa80c126930368"
)

ainp1 = messages.TxInputType(
    # tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu
    address_n=parse_path("m/44h/1h/0h/0/0"),
    amount=300000000,
    prev_hash=TXHASH_e38206,
    prev_index=0,
)

ainp2 = messages.TxInputType(
    # tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu
    address_n=parse_path("m/44h/1h/0h/0/0"),
    amount=300000000,
    prev_hash=TXHASH_aaf51e,
    prev_index=1,
    #script_type=messages.InputScriptType.PAYTOADDRESS,
    #script_pubkey=bytes.fromhex(
    #    "76a914a579388225827d9f2fe9014add644487808c695d88ac"
    #),
    #script_sig=bytes.fromhex(
    #    "47304402202495a38e5b368569a1a0c9fc95aa7e57a0dd5ae43f51300d7222dc139015233d022047833eaa571578f72c8468c8b537b36410388b7eb5001d75d1f4b954e1997d590121030e669acac1f280d1ddf441cd2ba5e97417bf2689e4bbec86df4f831bf9f7ffd0"
    #),
)

aout1 = messages.TxOutputType(
    address="tmJ1xYxP8XNTtCoDgvdmQPSrxh5qZJgy65Z",
    amount=300000000 + 300000000 - 1940,
    script_type=messages.OutputScriptType.PAYTOADDRESS,
)

txs= [{
	'txid': '0590332a59117c66d5b59d73f042f2e4ad55a8f4e4c047bfab07b72710737cc9',
	'output_no': 0,
	'script_asm': 'OP_DUP OP_HASH160 a579388225827d9f2fe9014add644487808c695d OP_EQUALVERIFY OP_CHECKSIG',
	'script_hex': '76a914a579388225827d9f2fe9014add644487808c695d88ac',
	'value': '0.15875722',
	'confirmations': 8,
	'time': 165092219,
	},
	{
	'txid': '1e797587f5de05e3c5f843917d7e3112d6790dd9a0da0ea64728a52c003bf46a',
	'output_no': 0,
	'script_asm': 'OP_DUP OP_HASH160 a579388225827d9f2fe9014add644487808c695d OP_EQUALVERIFY OP_CHECKSIG',
	'script_hex': '76a914a579388225827d9f2fe9014add644487808c695d88ac',
	'value': '0.16128125',
	'confirmations': 6,
	'time': 1650922525
	}, {
	'txid': '259f886923e6bf4aa77f5e0c715bb8883be0aa4dd68f482e084af8de1aa20ae7',
	'output_no': 0,
	'script_asm': 'OP_DUP OP_HASH160 a579388225827d9f2fe9014add644487808c695d OP_EQUALVERIFY OP_CHECKSIG',
	'script_hex': '76a914a579388225827d9f2fe9014add644487808c695d88ac',
	'value': '0.04192920',
	'confirmations': 6,
	'time': 1650922525}
]

TXHASH_0369ea = bytes.fromhex("0590332a59117c66d5b59d73f042f2e4ad55a8f4e4c047bfab07b72710737cc9")
binp1 = messages.TxInputType(
    # tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu
    #address_n=parse_path("m/44h/1h/0h/0/0"),
	address_n=parse_path("m/44h/133h/0h/0/0"),
    amount=300000000,
    prev_hash=TXHASH_0369ea,
    prev_index=0,
	#script_pubkey=bytes.fromhex("76a914a579388225827d9f2fe9014add644487808c695d88ac"),
)

bout1 = messages.TxOutputType(
    #address="tmJ1xYxP8XNTtCoDgvdmQPSrxh5qZJgy65Z",
	address="u1qld9m8deq56mpvma9gpvm5ths62f9fcqa9udwn7jvjts3msldpet509nnuguvl6zq0atz9s8t53wm207zq2xyhawanjg4xt2yzqvuwt6kzx2lzzmk9w45mlh6vmacmywmeh6c584t8u",
    amount=300000000 - 2000,
    script_type=messages.OutputScriptType.PAYTOADDRESS,
)


client = get_default_client()
sigs, ser = btc.sign_tx(
	client,
	#"Zcash Testnet",
	"Zcash",
	[binp1], #[ainp1, ainp2], #[inp1],
	[bout1], #[aout1], #[out1, out2, out3],
    version=5,
    version_group_id=0x26a7270a,
    branch_id=0xC2D6D0B4,
)
  #nVersionGroupId: 0a27a726
  #nConsensusBranchId: b4d0d6c2 0xC2D6D0B4

#print(sigs[0].hex())
#print(sigs[1].hex())
print(bytes.hex(ser))
