"""ToolkitVersion test suite"""

from moztoolkitversion import *

def test__construct():
    """ToolkitVersion Constructors/Parsers and reserialization"""

    assert "0" == ToolkitVersion()
    assert "0" == ToolkitVersion(None)
    assert "0" == ToolkitVersion(0)
    assert "0" == ToolkitVersion(0.0)
    assert "0" == ToolkitVersion("")
    assert "0" == ToolkitVersion(".")
    assert "0" == ToolkitVersion("..")
    assert "1" == ToolkitVersion("1")
    assert "1" == ToolkitVersion(1)
    assert "1" == ToolkitVersion(1.0)
    assert "1" == ToolkitVersion("1.0")
    assert "1" == ToolkitVersion("1..")
    assert "1.0a1" == ToolkitVersion("1.0a1")
    assert "1.0a1" == ToolkitVersion("1.a1")
    assert "1.1pre" == ToolkitVersion("1.+")
    assert "1pre.1pre" == ToolkitVersion("+.+")
    assert "1.2pre" == ToolkitVersion("1.1+")
    assert "1.2147483648" == ToolkitVersion("1.*")
    assert "1.0*.2147483648" == ToolkitVersion("1.*.*")

def test_parse():
    """Edgy version parsing"""

    versions = {"4.0.0": "4",
                "4.0b": "4.0b",
                "4.0.1": "4.0.1",
                "4.0.1.0": "4.0.1",
                "4.001": "4.1",
                "4.010": "4.10",
                "4..1": "4.0.1",
                "4.b1pre.1": "4.0b1pre.1",
                ".": "0",
                "": "0",
                "-1": "-1",
                "4.-01": "4.-1",
                "4.1b-01pre": "4.1b-1pre",
                "4.0pre0": "4.0pre",
                "4.0.0.0.0.0": "4",
                "4.....": "4"
                }
    for k, v in versions.items():
        assert v == ToolkitVersion(k)

def test_cmp_lt_gt():
    """Comparisons (less/greater)"""

    versions = {"": "1.-1",
                "1.-1": "1",
                "1": "1.1a",
                "1.1a": "1.1aa",
                "1.1aa": "1.1ab",
                "1.1ab": "1.1b",
                "1.1b": "1.1c",
                "1.1c": "1.1pre",
                "1.1pre": "1.1pre1a",
                "1.1pre": "1.1pre2",
                "1.1pre2": "1.1pre10",
                "1.1pre10": "1.1.-1",
                "1.1.-1": "1.10",
                "1.1.-1": "2.0.0.0",
                "2.0.0.0": "2.0.*",
                "2.0.*": "2.0+",
                "2.0+": "2.1",
                "2.1": "2.1+"
                }
    for k, v in versions.items():
        k, v = ToolkitVersion(k), ToolkitVersion(v)
        assert k < v
        assert v > k
        assert k != v

def test_cmp_coercion():
    """Comparisons (coercion)"""

    version = ToolkitVersion(1)
    versions = [1, 1.0, "1.", "1..", "1.0", "1..0", "1.0.0.0.0"]

    for v in versions:
        assert version == v
        assert v == version

def test_cmp_sort():
    """Comparisons (sorting)"""

    versions = ["",
                "1.-1",
                "1",
                "1.1a",
                "1.1aa",
                "1.1ab",
                "1.1b",
                "1.1c",
                "1.1pre",
                "1.1pre1a",
                "1.1pre2",
                "1.1pre10",
                "1.1.-1",
                "1.1",
                "1.10",
                "2.0.0.0"
                ]
    shuffled = ["",
                "1",
                "1.1a",
                "1.1ab",
                "1.1b",
                "1.-1",
                "1.1c",
                "2.0.0.0",
                "1.1pre",
                "1.10",
                "1.1pre2",
                "1.1aa",
                "1.1pre10",
                "1.1.-1",
                "1.1",
                "1.1pre1a"
                ]
    versions = [ToolkitVersion(v) for v in versions]
    shuffled = [ToolkitVersion(v) for v in shuffled]

    # identity
    assert versions == sorted(versions)
    # different
    assert versions != shuffled
    # reversed
    assert versions == sorted(reversed(versions))
    # reversed, different
    assert versions != reversed(versions)

    # shuffled
    assert versions == sorted(shuffled)
    # shuffled reverse
    assert versions == sorted(reversed(shuffled))
