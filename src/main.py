
from ngram_sampler import NGramSampler, SamplingMethod
from count_ngrams import count_ngrams_in_irealpro_file


if __name__ == "__main__":
    store = count_ngrams_in_irealpro_file("JazzStandards.json")
    sampler = NGramSampler(
        3,
        ["Dm7", "G7", "C6"],
        key_invariant_ngram=False,
        sampling_method=SamplingMethod.UNFIROM_SAMPLE,
    )

    for i in range(20):
        print(sampler.sample_next())

    print(sampler.chords)
