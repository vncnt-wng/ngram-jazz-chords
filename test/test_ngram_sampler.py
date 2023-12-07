import sys
sys.path.append("src/")

from ngram_store import NGramStore, NGram
from ngram_sampler import NGramSampler, SamplingMethod


def get_dummy_ngram_store() -> NGramStore:
    store = NGramStore(1)
    
    g7_count = NGram(1, "G7")
    g7_count.store = {"C" : 1}
    store.store["G7"] = g7_count
    
    c_count = NGram(1, "C")
    c_count.store = {"A7" : 1}
    store.store["C"] = c_count
    
    dm7_count = NGram(1, "A7")
    dm7_count.store = {"Dm7" : 2}
    store.store["A7"] = dm7_count
    
    return store


def get_dummy_invariant_ngram_store() -> NGramStore:
    store = NGramStore(1)
    
    b7_count = NGram(1, "[i]7")
    b7_count.store = {"[iv]" : 1}
    store.store["[i]7"] = b7_count
    
    return store



def test_sample_next_key_variant():
    store = get_dummy_ngram_store()
    sampler = NGramSampler(
        1,
        ["G7"],
        ngram_store=store,
        key_invariant_ngram=False
    )
    assert sampler.sample_next() == "C"
    assert sampler.sample_next() == "A7"
    assert sampler.sample_next() == "Dm7"
    
    

def test_sample_next_key_invariant():
    """
    the invariant ngram store only stores a v7 to root movement, assert sampling next from a v7 returns the root
    """
    store = get_dummy_invariant_ngram_store()
    sampler_f7 = NGramSampler(
        1,
        ["F7"],
        ngram_store=store,
        key_invariant_ngram=True,
        sampling_method=SamplingMethod.MOST_FREQUENT
    )
    assert sampler_f7.sample_next() == "Bb"
    
    
    sampler_c7 = NGramSampler(
        1,
        ["C7"],
        ngram_store=store,
        key_invariant_ngram=True,
        sampling_method=SamplingMethod.MOST_FREQUENT
    )
    assert sampler_c7.sample_next() == "F"