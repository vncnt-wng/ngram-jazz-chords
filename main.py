import json
from typing import List
from ngram import NGram, NGramStore
from intervals import (
    get_key_invariant_ngram,
    get_relative_chord_name,
    get_chord_root,
    get_concrete_chord_name,
)


def split_chord_string(chord_string: str) -> List[str]:
    norm_string = chord_string.replace(",", "|")
    return list(filter(lambda x: x != "", norm_string.split("|")))


"""
Form heading structure
 
    Sections:
        MainSegment:
            Chords
        (Endings):
            [Chords]

"""


def flatten_form(sections: any) -> List[str]:
    chord_list: List[str] = []
    for section in sections["Sections"]:
        chord_list += flatten_section(section)

    return chord_list


def flatten_section(section: any) -> List[str]:
    chord_list: List[str] = split_chord_string(section["MainSegment"]["Chords"])
    if "Endings" in section:
        for ending in section["Endings"]:
            chord_list += split_chord_string(ending["Chords"])
    return chord_list


def count_ngams_in_form(
    form: [str], ngram_store: NGramStore, n: int, key_invariant=False
) -> None:
    # we want to count ngrams wrapping from the end back to the start, ignoring adjacent duplicates
    wrapped_form = []
    for chord in form:
        if len(wrapped_form) == 0 or chord != wrapped_form[-1]:
            wrapped_form.append(chord)
            # if "/" in chord:
            #     print(chord)

    wrapped_form = wrapped_form + wrapped_form[:n]

    # circular queue for ngram window
    ngram_queue = form[:n]
    queue_pointer = 0

    # iterate over the length of the original form
    for i in range(0, len(wrapped_form) - n):
        ngram_string = ""
        next_chord = ""
        if key_invariant:
            # TODO - we don't properly handle chord bracketing yet - try catch to just ignore these for now
            try:
                ngram_chords = (
                    ngram_queue[queue_pointer:] + ngram_queue[0:queue_pointer]
                )
                relative_root = get_chord_root(ngram_chords[0])

                ngram_string = get_key_invariant_ngram(
                    ngram_chords,
                    relative_root=relative_root,
                )
                next_chord = get_relative_chord_name(wrapped_form[i + n], relative_root)
            except:
                continue
        else:
            ngram_string = "".join(ngram_queue[queue_pointer:]) + "".join(
                ngram_queue[0:queue_pointer]
            )
            next_chord = wrapped_form[i + n]
        ngram_store.add_count(ngram_string, next_chord)

        ngram_queue[queue_pointer] = wrapped_form[i + n]
        queue_pointer = (queue_pointer + 1) % n


# def count_ngrams(n: int):


def count_ngrams(key_invariant=False, n=2) -> NGramStore:
    with open("JazzStandards.json", "r") as f:
        j = json.load(f)
        ngram_store = NGramStore(n)

        for i in range(0, len(j)):
            # print()
            # print(ngram_store)
            form = flatten_form(j[i])
            count_ngams_in_form(form, ngram_store, n, key_invariant)

        # print(ngram_store)
        return ngram_store


def query_key_invariant_ngram(store: NGramStore, chord_names: List[str]):
    if len(chord_names) != store.n:
        raise ValueError("Length of chord_names does not match n of ngram store")
    relative_root = get_chord_root(chord_names[0])
    ngram_string = get_key_invariant_ngram(chord_names, relative_root)
    ngram_counts = store.store[ngram_string]
    for chord, count in ngram_counts.get_sorted_counts()[:50]:
        print(
            f"{get_concrete_chord_name(chord, relative_root)}: {round((count/ngram_counts.count) * 100, 1)}"
        )


if __name__ == "__main__":
    store = count_ngrams(key_invariant=True, n=2)
    query_key_invariant_ngram(store, ["Dm7", "G7"])
    print()
    store2 = count_ngrams(key_invariant=True, n=3)
    query_key_invariant_ngram(store2, ["Cmaj7", "Ebmaj7", "Abmaj7"])
