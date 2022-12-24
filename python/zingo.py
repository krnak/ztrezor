import subprocess
import json
import time

def call(command):
    # print(command)
    result = subprocess.run(
        [
            "zingo-cli",
            "--server", "https://testnet.lightwalletd.com:9067",
            *command,
        ],
        stdout=subprocess.PIPE,
    )
    while "\"result\": \"success\"" not in result.stdout.decode():
        time.sleep(1)
        print("waiting for zingo to connect")
    while "unspent_orchard_notes" not in result.stdout.decode():
        time.sleep(1)
        print("waiting for zingo notes")
    result = result.stdout.decode().split("Lightclient connecting to https://testnet.lightwalletd.com:9067/\n")[1]
    result = "{\n" + result.split("\n}\n{\n")[1]
    # print(f"\n\n{ result } \n\n")
    return json.loads(result)


def notes():
    return call(["notes"])


if __name__ == "__main__":
    print(notes())
