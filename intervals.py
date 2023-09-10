from typing import Dict

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


def get_interval(lower_note: str, upper_note: str):
    return interval_names[
        (note_name_values[upper_note] - note_name_values[lower_note] % 12)
    ]


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
    if len(chord_string) >= 2 and chord_string in ["b", "#"]:
        return chord_string[:2]
    return chord_string[:1]


def get_relative_chord_name(chord_name, relative_root) -> str:
    pass
