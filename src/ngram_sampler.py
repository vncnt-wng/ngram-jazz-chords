from typing import List
from enum import Enum
from random import random

from ngram_store import NGramStore
from intervals import (
    get_key_invariant_ngram,
    get_chord_root,
    get_concrete_chord_name,
)

class SamplingMethod(Enum):
    MOST_FREQUENT = 1
    UNFIROM_SAMPLE = 2
    TEMPERATURE = 3


class NGramSampler:
    n: int
    chords: [str]
    key_invariant_ngram: bool
    ngram_store: NGramStore
    sampling_method: SamplingMethod

    def __init__(
        self,
        n: int,
        initial_chords: [str],
        ngram_store: NGramStore,
        key_invariant_ngram=True,
        sampling_method=SamplingMethod.MOST_FREQUENT,
    ):
        self.n = n
        self.chords = initial_chords
        self.ngram_store = ngram_store
        self.key_invariant_ngram = key_invariant_ngram
        self.sampling_method = sampling_method

        # if not ngram_store:
        #     self.ngram_store = count_ngrams(key_invariant=key_invariant_ngram, n=n)

    def sample_next(self) -> str:
        # String for ngram chords, will either be concreate or invariant
        window = ""
        # Only used for key invariant
        relative_root = None

        if not self.key_invariant_ngram:
            window = "".join(self.chords[-self.n :])
        else:
            window = get_key_invariant_ngram(
                self.chords[-self.n :], relative_root=relative_root
            )
            relative_root = get_chord_root(self.chords[-self.n])

        # TODO how to handle key error? not keeping a vocab so can't really do +1 sampling

        ngram = self.ngram_store.store[window]
        # counts is a sorted list of dictinary k,v pairs of chord: counts for the chord
        counts = ngram.get_sorted_counts()
        chord = ""

        if self.sampling_method == SamplingMethod.MOST_FREQUENT:
            chord = counts[0][0]

        elif self.sampling_method == SamplingMethod.UNFIROM_SAMPLE:
            random_val = random()
            chord_set = False

            for potential_chord, count in counts:
                chord_proportion = count / ngram.count
                if chord_proportion > random_val:
                    chord = potential_chord
                    chord_set = True
                    break
                else:
                    random_val -= chord_proportion

            # If random val got to end of counts, return the last count
            if not chord_set:
                chord = counts[-1][0]

        
        if self.key_invariant_ngram:
            chord = get_concrete_chord_name(chord, relative_root=relative_root)

        self.chords.append(chord)
        return chord

    def sample_n(self, num_samples: int) -> List[str]:
        pass
