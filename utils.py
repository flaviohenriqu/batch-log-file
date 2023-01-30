from immudb.client import ImmudbClient
import itertools


def chunked(it, size):
    it = iter(it)
    while True:
        p = dict(itertools.islice(it, size))
        if not p:
            break
        yield p
