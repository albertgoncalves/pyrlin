#!/usr/bin/env python3

from numba import njit
from numpy import empty, float32

from grid import N_COL, N_ROW

# Interpolation
RES = 100
RES_N_ROW = (N_ROW - 1) * RES  # y, i
RES_N_COL = (N_COL - 1) * RES  # x, j
RES_N = RES_N_ROW * RES_N_COL


@njit
def select(xs, j, i):
    return xs[j + (i * N_COL)]


@njit
def dot_grid_gradient(cxs, cys, j, i, x, y):
    dx = x - float32(j)
    dy = y - float32(i)
    return ((dx * select(cxs, j, i)) + (dy * select(cys, j, i)))


@njit
def lerp(a, b, w):
    return a + (w * (b - a))


@njit
def perlin(cxs, cys, x, y):
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1
    sx = x - float32(x0)
    sy = y - float32(y0)
    n0 = dot_grid_gradient(cxs, cys, x0, y0, x, y)
    n1 = dot_grid_gradient(cxs, cys, x1, y0, x, y)
    m0 = dot_grid_gradient(cxs, cys, x0, y1, x, y)
    m1 = dot_grid_gradient(cxs, cys, x1, y1, x, y)
    return lerp(lerp(n0, n1, sx), lerp(m0, m1, sx), sy)


@njit
def iterate(xs, ys, cxs, cys):
    zs = empty(RES_N, dtype=float32)
    for ij in range(RES_N):
        i = (ij // RES_N_COL) / float32(RES)
        j = (ij % RES_N_COL) / float32(RES)
        zs[ij] = perlin(cxs, cys, j, i)
    return zs
