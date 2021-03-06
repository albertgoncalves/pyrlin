#!/usr/bin/env python3

from numba import njit, prange
from numpy import empty, float32, max, min

import timer


@njit
def dot_grid_gradient(vxs, vys, n, n_col, j, i, x, y):
    # NOTE: xs[i, j] -> xs[(j + (i * n_col)) % n]
    return ((x - float32(j)) * vxs[(j + (i * n_col)) % n]) + \
        ((y - float32(i)) * vys[(j + (i * n_col)) % n])


@njit
def lerp(a, b, w):
    return a + (w * (b - a))


@njit
def fade(x):
    return x * x * x * (x * ((x * 6.0) - 15.0) + 10.0)


@njit
def perlin(vxs, vys, n, n_col, x, y):
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1
    sx = fade(x - float32(x0))
    sy = fade(y - float32(y0))
    return lerp(
        lerp(
            dot_grid_gradient(vxs, vys, n, n_col, x0, y0, x, y),
            dot_grid_gradient(vxs, vys, n, n_col, x1, y0, x, y),
            sx,
        ),
        lerp(
            dot_grid_gradient(vxs, vys, n, n_col, x0, y1, x, y),
            dot_grid_gradient(vxs, vys, n, n_col, x1, y1, x, y),
            sx,
        ),
        sy,
    )


@timer.info_timing
@njit(parallel=True)
def iterate(
    xs,
    ys,
    vxs,
    vys,
    n,
    n_col,
    n_row,
    resolution,
    octaves,
    persistence,
):
    res_n_col = (n_col - 1) * resolution  # x, j
    res_n_row = (n_row - 1) * resolution  # y, i
    res_n = res_n_col * res_n_row
    res = float32(resolution)
    zs = empty(res_n, dtype=float32)
    for ij in prange(res_n):
        z = 0
        freq = 1
        amp = 1
        for _ in range(octaves):
            z += perlin(
                vxs,
                vys,
                n,
                n_col,
                freq * ((ij % res_n_col) / res),
                freq * ((ij // res_n_col) / res),
            ) * amp
            freq *= 2
            amp *= persistence
        zs[ij] = z
    return (zs, res_n_col, res_n_row)


def normalize(xs):
    xs -= min(xs)
    xs /= max(xs)
    return xs
