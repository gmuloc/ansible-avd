# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

import pytest

from pyavd._schema.models.avd_path import AvdPath, PathIndexedListKey

PATH_INDEXED_LIST_KEY_TESTS = [pytest.param((1, "Ethernet1", "name"), "[1 | name=Ethernet1]", id="Valid Key")]

AVD_PATH_TESTS = [
    pytest.param([], "", id="Root Path"),
    pytest.param(
        ["ethernet_interfaces", PathIndexedListKey(0, "Ethernet1", "name")],
        "ethernet_interfaces[0 | name=Ethernet1]",
        id="Path with PathIndexedListKey at the end",
    ),
    pytest.param(
        ["ethernet_interfaces", PathIndexedListKey(0, "Ethernet1", "name"), "speed"],
        "ethernet_interfaces[0 | name=Ethernet1].speed",
        id="Path with PathIndexedListKey",
    ),
    pytest.param(["ethernet_interfaces", "stuff", "blah", "46"], "ethernet_interfaces.stuff.blah.46", id="Only str"),
    pytest.param(["ethernet_interfaces", "stuff", "blah", 42, "46"], "ethernet_interfaces.stuff.blah[42].46", id="Int"),
]

AVD_PATH_PARENT_TESTS = [
    pytest.param([], "", id="Root Path"),
    pytest.param(["ethernet_interfaces", PathIndexedListKey(0, "Ethernet1", "name")], "ethernet_interfaces", id="Path with PathIndexedListKey at the end"),
    pytest.param(
        ["ethernet_interfaces", PathIndexedListKey(0, "Ethernet1", "name"), "speed"],
        "ethernet_interfaces[0 | name=Ethernet1]",
        id="Path with PathIndexedListKey",
    ),
    pytest.param(["ethernet_interfaces", "stuff", "blah", "46"], "ethernet_interfaces.stuff.blah", id="Only str"),
    pytest.param(["ethernet_interfaces", "stuff", "blah", 42, "46"], "ethernet_interfaces.stuff.blah[42]", id="Int"),
]

AVD_PATH_DESCENDANT_TESTS = [
    pytest.param([], ["test"], "test", id="Single Key on root"),
    pytest.param([], ["test", 42], "test[42]", id="Multiple keys on root including int"),
    pytest.param(
        ["ethernet_interfaces", PathIndexedListKey(0, "Ethernet1", "name")], ["speed"], "ethernet_interfaces[0 | name=Ethernet1].speed", id="single key"
    ),
    pytest.param(
        ["ethernet_interfaces", PathIndexedListKey(0, "Ethernet1", "name")],
        ["speed", 42],
        "ethernet_interfaces[0 | name=Ethernet1].speed",
        id="multiple keys with int",
    ),
    pytest.param(
        ["ethernet_interfaces", PathIndexedListKey(0, "Ethernet1", "name")],
        ["speed", 42, "sublist", PathIndexedListKey(666, "blah", "example")],
        "ethernet_interfaces[0 | name=Ethernet1].speed[42].sublist[666 | example=blah]",
        id="multiple keys with PathIndexedListKey",
    ),
]


class TestPathIndexedListKey:
    def test___str__(self, test_value: tuple[int, str, str], expected_output: str) -> None:
        assert str(PathIndexedListKey(*test_value)) == expected_output


class TestAvdPath:
    @pytest.mark.parametrize(("test_value", "expected_output"), AVD_PATH_TESTS)
    def test__str__(self, test_value: list[int | str | PathIndexedListKey], expected_output: str) -> None:
        assert str(AvdPath(*test_value)) == expected_output

    @pytest.mark.parametrize(("test_value", "expected_output"), AVD_PATH_PARENT_TESTS)
    def test_parent(self, test_value: list[int | str | AvdPath], expected_output: str) -> None:
        assert str(AvdPath(*test_value).parent) == expected_output

    @pytest.mark.parametrize(("test_value", "child_relative_path", "expected_output"), AVD_PATH_DESCENDANT_TESTS)
    def test_create_descendant(self, test_value: list[int | str | AvdPath], child_relative_path: list[int | str | AvdPath], expected_output: str) -> None:
        assert str(AvdPath(*test_value).create_descendant(child_relative_path)) == expected_output
