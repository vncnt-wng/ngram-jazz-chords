import sys

sys.path.append("src/")

import main as main
import ngram as ngram


def test_count_ngrams_unigram():
    form = ["Dm7", "G7", "Dm7", "C6"]
    store = ngram.NGramStore(1)
    main.count_ngams_in_form(form, store, 1)

    assert "Dm7" in store.store
    assert "G7" in store.store
    assert "C6" in store.store

    assert store.store["Dm7"].count == 2
    assert store.store["Dm7"].store["G7"] == 1
    assert store.store["Dm7"].store["C6"] == 1

    assert store.store["G7"].count == 1
    assert store.store["G7"].store["Dm7"] == 1

    assert store.store["C6"].count == 1
    assert store.store["C6"].store["Dm7"] == 1


def test_count_ngrams_unigram_no_repeats():
    form = ["Dm7", "Dm7", "G7", "Dm7", "C6", "C6"]
    store = ngram.NGramStore(1)
    main.count_ngams_in_form(form, store, 1)

    assert "Dm7" in store.store
    assert "G7" in store.store
    assert "C6" in store.store

    assert store.store["Dm7"].count == 2
    assert store.store["Dm7"].store["G7"] == 1
    assert store.store["Dm7"].store["C6"] == 1

    assert store.store["G7"].count == 1
    assert store.store["G7"].store["Dm7"] == 1

    assert store.store["C6"].count == 1
    assert store.store["C6"].store["Dm7"] == 1


def test_count_ngrams_trigram():
    form = ["Dm7", "G7", "Dm7", "C6"]
    store = ngram.NGramStore(3)
    main.count_ngams_in_form(form, store, 3)

    assert "Dm7G7Dm7" in store.store
    assert "G7Dm7C6" in store.store
    assert "Dm7C6Dm7" in store.store
    assert "C6Dm7G7" in store.store

    assert store.store["Dm7G7Dm7"].count == 1
    assert store.store["Dm7G7Dm7"].store["C6"] == 1

    assert store.store["G7Dm7C6"].count == 1
    assert store.store["G7Dm7C6"].store["Dm7"] == 1

    assert store.store["Dm7C6Dm7"].count == 1
    assert store.store["Dm7C6Dm7"].store["G7"] == 1

    assert store.store["C6Dm7G7"].count == 1
    assert store.store["C6Dm7G7"].store["Dm7"] == 1


def test_count_ngrams_key_invariance():
    form = ["Dm7", "G7", "Dm7", "C6"]
    store = ngram.NGramStore(3)
    main.count_ngams_in_form(form, store, 3, key_invariant=True)

    print(store)
    assert "[i]m7[iv]7[i]m7" in store.store
    assert "[i]7[v]m7[iv]6" in store.store
    assert "[i]m7[bvii]6[i]m7" in store.store
    assert "[i]6[ii]m7[v]7" in store.store

    assert store.store["[i]m7[iv]7[i]m7"].count == 1
    assert store.store["[i]m7[iv]7[i]m7"].store["[bvii]6"] == 1

    assert store.store["[i]7[v]m7[iv]6"].count == 1
    assert store.store["[i]7[v]m7[iv]6"].store["[v]m7"] == 1

    assert store.store["[i]m7[bvii]6[i]m7"].count == 1
    assert store.store["[i]m7[bvii]6[i]m7"].store["[iv]7"] == 1

    assert store.store["[i]6[ii]m7[v]7"].count == 1
    assert store.store["[i]6[ii]m7[v]7"].store["[ii]m7"] == 1
