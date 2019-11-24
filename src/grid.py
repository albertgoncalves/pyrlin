#!/usr/bin/env python3

from math import cos, pi, sin, sqrt
from random import random

from numpy import empty, float32

PI_2 = 2.0 * pi
UNIT = sqrt((0.5 * 0.5) + (0.5 * 0.5))

N_ROW = 9   # y, i
N_COL = 15  # x, j
N = N_ROW * N_COL


def point_on_unit_circle():
    theta = PI_2 * random()
    return (cos(theta) * UNIT, sin(theta) * UNIT)


def init():
    kwargs = {"dtype": float32}
    xs = empty(N, **kwargs)
    ys = empty(N, **kwargs)
    cxs = empty(N, **kwargs)
    cys = empty(N, **kwargs)
    for ij in range(N):
        xs[ij] = float32(ij % N_COL)
        ys[ij] = float32(ij // N_COL)
        (cx, cy) = point_on_unit_circle()
        cxs[ij] = cx
        cys[ij] = cy
    return (xs, ys, cxs, cys)
