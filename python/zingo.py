import subprocess
import json
import time

def call(command):
    # print(command)
    result = subprocess.run(
        [
            "/home/agi/jarys/zingolib/target/release/zingo-cli",
            "--server", "127.0.0.1:9067",
            *command,
        ],
        stdout=subprocess.PIPE,
    )
    while "{\n  \"result\": \"success\"\n}\n" not in result.stdout.decode():
        time.sleep(0.1)
    while "unspent_orchard_notes" not in result.stdout.decode():
        time.sleep(0.1)
    result = result.stdout.decode().split("{\n  \"result\": \"success\"\n}\n")[1]
    print(f"\n\n{ result } \n\n")
    return json.loads(result)


def notes():
    return call(["notes"])
