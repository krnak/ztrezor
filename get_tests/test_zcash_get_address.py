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

from trezorlib import zcash
from trezorlib.debuglink import TrezorClientDebugLink as Client
from trezorlib.exceptions import TrezorFailure
from trezorlib.messages import (
    ZcashGetAddress,
    ZcashGetFullViewingKey,
    ZcashGetIncomingViewingKey,
)
from trezorlib.tools import parse_path


def test_get_t_address(client):
    assert (
        zcash.get_address(
            client,
            t_address_n=parse_path("m/44h/133h/0h/0/0"),
        )
        == ""
    )
    assert (
        zcash.get_address(
            client,
            t_address_n=parse_path("m/44h/133h/1h/0/0"),
        )
        == ""
    )
    assert (
        zcash.get_address(
            client,
            t_address_n=parse_path("m/44h/133h/0h/0/1"),
        )
        == ""
    )


def test_get_u_address(client):
    assert (
        zcash.get_address(
            client,
            t_address_n=parse_path("m/44h/133h/0h/0/0"),
            z_address_n=parse_path("m/32h/133h/0h"),
        )
        == ""
    )
    assert (
        zcash.get_address(
            client,
            t_address_n=parse_path("m/44h/133h/1h/0/0"),
            z_address_n=parse_path("m/32h/133h/1h"),
        )
        == ""
    )
    assert (
        zcash.get_address(
            client,
            t_address_n=parse_path("m/44h/133h/3h/0/666"),
            z_address_n=parse_path("m/32h/133h/3h"),
            diversifier_index=666,
        )
        == ""
    )

    assert (
        zcash.get_address(
            client,
            t_address_n=None,
            z_address_n=parse_path("m/32h/133h/8h"),
            diversifier_index=42,
        )
        == ""
    )


def test_get_fvk(client):
    pass


def test_get_ivk(client):
    pass
