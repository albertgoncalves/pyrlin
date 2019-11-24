#!/usr/bin/env python3

from math import cos, pi, sin, sqrt
from random import random

from numpy import empty, float32

PI_2 = 2.0 * pi
UNIT = sqrt((0.5 * 0.5) + (0.5 * 0.5))


def point_on_unit_circle():
    theta = PI_2 * random()
    return (cos(theta) * UNIT, sin(theta) * UNIT)


def init(n, n_col, n_row):
    kwargs = {"dtype": float32}
    xs = empty(n, **kwargs)
    ys = empty(n, **kwargs)
    cxs = empty(n, **kwargs)
    cys = empty(n, **kwargs)
    for ij in range(n):
        xs[ij] = float32(ij % n_col)
        ys[ij] = float32(ij // n_col)
        (cx, cy) = point_on_unit_circle()
        cxs[ij] = cx
        cys[ij] = cy
    return (xs, ys, cxs, cys)
