#!/usr/bin/env python3

from logging import info
from time import time


def info_timing(func):
    def f(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        info("\033[1m{:>28}\033[0m: {:.4f}s".format(
            func.__name__,
            end - start,
        ))
        return result
    return f
