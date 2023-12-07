import sys

sys.path.append("src/")

from intervals import (
    get_interval,
    get_note,
    get_chord_root,
    get_relative_chord_name,
    get_key_invariant_ngram,
    get_concrete_chord_name
)

def test_get_interval():
    assert get_interval("C", "G") == "v"
    assert get_interval("B", "C") == "bii"
    assert get_interval("F", "C") == "v"
    assert get_interval("F", "F") == "i"


def test_get_note():
    assert get_note("i", "C") == "C"
    assert get_note("i", "F") == "F"
    assert get_note("v", "C") == "G"
    assert get_note("v", "F") == "C"
    assert get_note("bii", "B") == "C"


def test_get_chord_root_simple():
    assert get_chord_root("C") == "C"
    assert get_chord_root("G#") == "G#"
    assert get_chord_root("Fbasjkghsjl") == "Fb"


def test_get_relative_chord_name_simple():
    assert get_relative_chord_name("C", "C") == "[i]"
    assert get_relative_chord_name("C#maj7", "C") == "[bii]maj7"
    assert get_relative_chord_name("C7sus4", "D") == "[bvii]7sus4"


def test_get_relative_chord_name_slash():
    """
    Tests that when multiple note names in a chord are transformed to the interval
    """
    assert get_relative_chord_name("C#/A", "A") == "[iii]/[i]"
    assert get_relative_chord_name("C#7/B", "A") == "[iii]7/[ii]"


def test_get_key_invariant_ngram():
    assert get_key_invariant_ngram(["C"]) == "[i]"
    assert get_key_invariant_ngram(["C", "G", "D"]) == "[i][v][ii]"
    assert get_key_invariant_ngram(["Cm7", "G7", "D6"]) == "[i]m7[v]7[ii]6"


def test_get_concrete_chord_name_simple():
    assert get_concrete_chord_name("[i]", "C") == "C"
    assert get_concrete_chord_name("[bii]maj7", "C") == "C#maj7"
    assert get_concrete_chord_name("[bvii]7sus4", "D") == "C7sus4"


def test_get_concrete_chord_name_slash():
    """
    Tests that multiple note names in a chord are transformed to the interval
    """
    assert get_concrete_chord_name("[iii]/[i]", "A") == "C#/A"
    assert get_concrete_chord_name("[iii]7/[ii]", "A") == "C#7/B"
