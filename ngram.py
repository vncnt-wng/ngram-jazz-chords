from __future__ import annotations
from typing import Dict


class NGramStore:
    # size of ngram
    n: int
    # map of ngram string to its store
    store: Dict[str, NGram]

    def __init__(self, n):
        self.n = n
        self.store = dict()

    def add_count(self, ngram: str, next: str):
        if ngram in self.store:
            self.store[ngram].add_count(next)
        else:
            new_ngram = NGram(self.n, ngram)
            new_ngram.add_count(next)
            self.store[ngram] = new_ngram

    def __str__(self):
        string = ""
        sorted_items = sorted(
            self.store.items(), key=lambda i: i[1].count, reverse=True
        )
        for ngram, store in sorted_items[:30]:
            string += f"{ngram}: {store.count}\n"
        return string


class NGram:
    # size of ngram
    n: int
    # ngram string
    ngram: str
    # total occurrences
    count: int
    # map of next in sequence to count
    store: Dict[str, int]

    def __init__(self, n, ngram):
        self.n = n
        self.ngram = ngram
        self.count = 0
        self.store = dict()

    def add_count(self, next):
        self.count += 1
        if next in self.store:
            self.store[next] += 1
        else:
            self.store[next] = 1

    def __str__(self):
        string = ""
        sorted_items = sorted(self.store.items(), key=lambda i: i[1], reverse=True)
        string += f"ngram: {self.ngram}\n"

        for next, count in sorted_items[:30]:
            string += f"{next}: {count}\n"
        return string
