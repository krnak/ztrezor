#! /usr/bin/python

from cases import CASES
import os

HEADER = """\
# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import pytest

from trezorlib import messages, zcash
from trezorlib.debuglink import TrezorClientDebugLink as Client
from trezorlib.exceptions import TrezorFailure
from trezorlib.messages import (
    ButtonRequest,
    OutputScriptType,
    RequestType as T,
    TxInputType,
    TxOutputType,
    TxRequest,
    TxRequestDetailsType,
    ZcashOrchardInput,
    ZcashOrchardOutput,
    ZcashSignatureType,
    Failure,
    FailureType,
)
from trezorlib.tools import parse_path

from ..bitcoin.signtx import request_finished, request_input, request_output

B = messages.ButtonRequestType


def request_orchard_input(i: int):
    return TxRequest(
        request_type=T.TXORCHARDINPUT,
        details=messages.TxRequestDetailsType(request_index=i),
    )


def request_orchard_output(i: int):
    return TxRequest(
        request_type=T.TXORCHARDOUTPUT,
        details=messages.TxRequestDetailsType(request_index=i),
    )


def request_no_op():
    return TxRequest(request_type=T.NO_OP)


"""

with open("/home/agi/tfw/tests/device_tests/zcash/test_sign_shielded_tx.py", "w") as file:
    file.write(HEADER)
    for case in CASES:
        case.gen_expected()
        case.render()
        case.save()
    for filename in os.listdir("/home/agi/gh/jarys/ztrezor/rendered"):
        if not filename.startswith("funding") and filename != "all.py":
            with open(f"/home/agi/gh/jarys/ztrezor/rendered/{filename}") as f:
                file.write(f.read())
                file.write("\n\n")