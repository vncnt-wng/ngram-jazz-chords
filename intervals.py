import re
from typing import Dict, List

note_name_values: Dict[str, int] = {
    "B#": 0,
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "Fb": 4,
    "E#": 5,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
    "Cb": 11,
}

# index denotes the size of the interval in semitones
interval_names = [
    "i",
    "bii",
    "ii",
    "biii",
    "iii",
    "iv",
    "bv",
    "v",
    "bvi",
    "vi",
    "bvii",
    "vii",
]

# TODO provide the actual enharmonic note name for the given key
# index denotes the value
easy_note_names = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]


def get_interval(lower_note: str, upper_note: str) -> str:
    return interval_names[
        (note_name_values[upper_note] - note_name_values[lower_note] % 12)
    ]


def get_note(interval: str, relative_root: str) -> str:
    degree = interval_names.index(interval) + note_name_values[relative_root]
    return easy_note_names[degree % 12]


"""
ngrams and target chord relative to root of FIRST chord in ngram 

replace all note names in place. Note names will always be capital letter, maybe with flat or sharp

how to switch back from invariant to the chord names when given 

"""


def get_chord_root(chord_string: str) -> str:
    # IGNORE SLASH CHORDS FOR NOW - this function should only be used to get a relative root to make the ngram invariant so reall
    # if is a slash chord
    # parts = chord_string.split("/")
    # if len(parts) > 1:
    if len(chord_string) >= 2 and chord_string[1] in ["b", "#"]:
        return chord_string[:2]
    return chord_string[:1]


def replace_note_match_with_interval(note_match: any, relative_root: str) -> str:
    return "[" + get_interval(relative_root, note_match.group(0)) + "]"


def get_relative_chord_name(chord_string: str, relative_root: str) -> str:
    note_pattern = r"[A-G][b#]?"
    return re.sub(
        note_pattern,
        lambda x: replace_note_match_with_interval(x, relative_root),
        chord_string,
    )


def replace_interval_match_with_note(interval_match: any, relative_root: str):
    interval = interval_match.group(0)[1:-1]
    return get_note(interval, relative_root)


def get_concrete_chord_name(relative_chord_string: str, relative_root: str) -> str:
    interval_pattern = r"\[(.*?)\]"
    return re.sub(
        interval_pattern,
        lambda x: replace_interval_match_with_note(x, relative_root),
        relative_chord_string,
    )


def get_key_invariant_ngram(chord_names: List[str], relative_root: str = None) -> str:
    """
    returns a concatenated string of chord_names, with note names switched to intervals
    relative to the root of the first chord in chord_names


    """
    if relative_root == None:
        relative_root = get_chord_root(chord_names[0])

    ngram_string = ""
    for chord_string in chord_names:
        print(chord_string)
        ngram_string += get_relative_chord_name(chord_string, relative_root)
    print(ngram_string)
    return ngram_string
