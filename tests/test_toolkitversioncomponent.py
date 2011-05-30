"""ToolkitVersionComponent test suite"""

from moztoolkitversion import *
from nose.tools import raises

def test__construct():
    """ToolkitVersionComponent constructors/parser"""
    assert ToolkitVersionComponent() == ToolkitVersionComponent()
    assert ToolkitVersionComponent() == ToolkitVersionComponent("")
    assert ToolkitVersionComponent() == ToolkitVersionComponent("0")
    assert ToolkitVersionComponent(1) == ToolkitVersionComponent("1")
    assert ToolkitVersionComponent("0b") == ToolkitVersionComponent("b")

def test_repr_():
    """Representation/string serialization"""
    assert "0" == str(ToolkitVersionComponent())
    assert "0" == str(ToolkitVersionComponent(""))
    assert "0" == str(ToolkitVersionComponent("0"))
    assert "0b" == str(ToolkitVersionComponent("b"))
    assert "0b" == str(ToolkitVersionComponent("b0"))
    assert "0b1" == str(ToolkitVersionComponent("b1"))
    assert "0b1pre" == str(ToolkitVersionComponent("b1pre"))
    assert "1b" == str(ToolkitVersionComponent("1b"))
    assert "1b" == str(ToolkitVersionComponent("1b0"))
    assert "1b1" == str(ToolkitVersionComponent("1b1"))
    assert "1b1pre" == str(ToolkitVersionComponent("1b1pre"))
    assert "1b1pre1" == str(ToolkitVersionComponent("1b1pre1"))
    assert "1b1pre1" == str(ToolkitVersionComponent("01b01pre1"))
    assert "1b1pre01" == str(ToolkitVersionComponent("01b01pre01"))

@raises(ValueError)
def test_cmp_int():
    """Component comparison (int)"""
    ToolkitVersionComponent() == 0

@raises(ValueError)
def test_cmp_float():
    """Component comparison (float)"""
    ToolkitVersionComponent() == 0.0

@raises(ValueError)
def test_cmp_str():
    """Component comparison (str)"""
    ToolkitVersionComponent() == "0"

def test_to_tuple():
    """to_tuple serialization"""
    assert [0, "", 0, ""] == ToolkitVersionComponent().to_tuple()
    assert [1, "b", 1, "pre1"] == ToolkitVersionComponent("1b1pre1").to_tuple()
