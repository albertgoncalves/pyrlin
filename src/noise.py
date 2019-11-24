#!/usr/bin/env python3

# https://en.wikipedia.org/wiki/Perlin_noise
# https://longwelwind.net/2017/02/09/perlin-noise.html
# https://rmarcus.info/blog/2018/03/04/perlin-noise.html

from numba import njit
from numpy import empty, float32

from grid import N_COL, N_ROW

RES = 200
RES_N_COL = (N_COL - 1) * RES  # x, j
RES_N_ROW = (N_ROW - 1) * RES  # y, i
RES_N = RES_N_COL * RES_N_ROW


@njit
def select(xs, j, i):
    return xs[j + (i * N_COL)]


@njit
def dot_grid_gradient(cxs, cys, j, i, x, y):
    return ((x - float32(j)) * select(cxs, j, i)) + \
        ((y - float32(i)) * select(cys, j, i))


@njit
def lerp(a, b, w):
    return a + (w * (b - a))


@njit
def fade(x):
    return (6.0 * x * x * x * x * x) - \
        (15.0 * x * x * x * x) + \
        (10.0 * x * x * x)


@njit
def perlin(cxs, cys, x, y):
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1
    sx = fade(x - float32(x0))
    sy = fade(y - float32(y0))
    return lerp(
        lerp(
            dot_grid_gradient(cxs, cys, x0, y0, x, y),
            dot_grid_gradient(cxs, cys, x1, y0, x, y),
            sx,
        ),
        lerp(
            dot_grid_gradient(cxs, cys, x0, y1, x, y),
            dot_grid_gradient(cxs, cys, x1, y1, x, y),
            sx,
        ),
        sy,
    )


@njit
def iterate(xs, ys, cxs, cys):
    zs = empty(RES_N, dtype=float32)
    for ij in range(RES_N):
        zs[ij] = perlin(
            cxs,
            cys,
            (ij % RES_N_COL) / float32(RES),
            (ij // RES_N_COL) / float32(RES),
        )
    return zs
