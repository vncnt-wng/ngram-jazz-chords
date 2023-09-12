import sys

sys.path.append("../")

import intervals


def test_get_interval():
    assert intervals.get_interval("C", "G") == "v"
    assert intervals.get_interval("B", "C") == "bii"
    assert intervals.get_interval("F", "C") == "v"
    assert intervals.get_interval("F", "F") == "i"


def test_get_note():
    assert intervals.get_note("i", "C") == "C"
    assert intervals.get_note("i", "F") == "F"
    assert intervals.get_note("v", "C") == "G"
    assert intervals.get_note("v", "F") == "C"
    assert intervals.get_note("bii", "B") == "C"


def test_get_chord_root_simple():
    assert intervals.get_chord_root("C") == "C"
    assert intervals.get_chord_root("G#") == "G#"
    assert intervals.get_chord_root("Fbasjkghsjl") == "Fb"


def test_get_relative_chord_name_simple():
    assert intervals.get_relative_chord_name("C", "C") == "[i]"
    assert intervals.get_relative_chord_name("C#maj7", "C") == "[bii]maj7"
    assert intervals.get_relative_chord_name("C7sus4", "D") == "[bvii]7sus4"


def test_get_relative_chord_name_slash():
    """
    Tests that when multiple note names in a chord are transformed to the interval
    """
    assert intervals.get_relative_chord_name("C#/A", "A") == "[iii]/[i]"
    assert intervals.get_relative_chord_name("C#7/B", "A") == "[iii]7/[ii]"


def test_get_concrete_chord_name_simple():
    assert intervals.get_concrete_chord_name("[i]", "C") == "C"
    assert intervals.get_concrete_chord_name("[bii]maj7", "C") == "C#maj7"
    assert intervals.get_concrete_chord_name("[bvii]7sus4", "D") == "C7sus4"


def test_get_concrete_chord_name_slash():
    """
    Tests that when multiple note names in a chord are transformed to the interval
    """
    assert intervals.get_concrete_chord_name("[iii]/[i]", "A") == "C#/A"
    assert intervals.get_concrete_chord_name("[iii]7/[ii]", "A") == "C#7/B"
