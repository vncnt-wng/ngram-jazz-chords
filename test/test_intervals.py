import sys

sys.path.append("../")

import intervals


def test_get_interval():
    assert intervals.get_interval("C", "G") == "v"
    assert intervals.get_interval("B", "C") == "bii"
    assert intervals.get_interval("F", "C") == "v"
    assert intervals.get_interval("F", "F") == "i"


def test_get_chord_root_simple():
    assert intervals.get_chord_root("Fbasjkghsjl") == "Fb"


# def test_get_chord_root_slash():
#     pass

# def test_get_chord_root_bracket():
#     pass
