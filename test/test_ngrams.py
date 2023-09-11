import sys

sys.path.append("../")

import main
import ngram


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
    store = ngram.NGramStore(1)
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
