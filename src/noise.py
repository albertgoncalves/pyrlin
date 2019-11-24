#!/usr/bin/env python3

from numba import njit
from numpy import empty, float32


@njit
def select(xs, j, i, n_col):
    return xs[j + (i * n_col)]


@njit
def dot_grid_gradient(vxs, vys, n_col, j, i, x, y):
    return ((x - float32(j)) * select(vxs, j, i, n_col)) + \
        ((y - float32(i)) * select(vys, j, i, n_col))


@njit
def lerp(a, b, w):
    return a + (w * (b - a))


@njit
def fade(x):
    return x * x * x * (x * ((x * 6.0) - 15.0) + 10.0)


@njit
def perlin(vxs, vys, n_col, x, y):
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1
    sx = fade(x - float32(x0))
    sy = fade(y - float32(y0))
    return lerp(
        lerp(
            dot_grid_gradient(vxs, vys, n_col, x0, y0, x, y),
            dot_grid_gradient(vxs, vys, n_col, x1, y0, x, y),
            sx,
        ),
        lerp(
            dot_grid_gradient(vxs, vys, n_col, x0, y1, x, y),
            dot_grid_gradient(vxs, vys, n_col, x1, y1, x, y),
            sx,
        ),
        sy,
    )


@njit
def iterate(xs, ys, vxs, vys, n_col, n_row, res):
    res_n_col = (n_col - 1) * res  # x, j
    res_n_row = (n_row - 1) * res  # y, i
    res_n = res_n_col * res_n_row
    zs = empty(res_n, dtype=float32)
    for ij in range(res_n):
        zs[ij] = perlin(
            vxs,
            vys,
            n_col,
            (ij % res_n_col) / float32(res),
            (ij // res_n_col) / float32(res),
        )
    return (zs, res_n_col, res_n_row)
