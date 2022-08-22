#!/usr/bin/env python3

import subprocess
import sys

try:
	tx_raw = sys.argv[1]
except IndexError:
	try:
		with open("/home/agi/tx") as file:
			tx_raw = file.read()
		print("loading tx from file")
	except FileNotFoundError:
		tx_raw = input("tx: ")
		print(tx_raw, len(set(tx_raw)))

subprocess.run(["zcash-cli", "sendrawtransaction", tx_raw.strip()])
