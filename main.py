import json
from typing import List
from ngram import NGram, NGramStore


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


def count_ngams_in_form(form: [str], ngram_store: NGramStore, n: int) -> None:
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
        ngram_string = "".join(ngram_queue[queue_pointer:]) + "".join(
            ngram_queue[0:queue_pointer]
        )
        ngram_store.add_count(ngram_string, wrapped_form[i + n])

        ngram_queue[queue_pointer] = wrapped_form[i + n]
        queue_pointer = (queue_pointer + 1) % n


# def count_ngrams(n: int):


def count_ngrams() -> NGramStore:
    with open("JazzStandards.json", "r") as f:
        j = json.load(f)
        n = 3
        ngram_store = NGramStore(n)

        for i in range(0, len(j)):
            # print()
            # print(ngram_store)
            form = flatten_form(j[i])
            count_ngams_in_form(form, ngram_store, n)

        # print(ngram_store)
        return ngram_store


if __name__ == "__main__":
    count_ngrams()
