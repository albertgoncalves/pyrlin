#!/usr/bin/env python3

from os import environ
from random import seed
from time import time
from sys import argv

from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.pyplot import arrow, close, savefig, subplots, tight_layout
from numpy import max, min

import grid
import noise

WD = environ["WD"]


def get_args():
    try:
        return (
            int(argv[1]),
            int(argv[2]),
            int(argv[3]),
            int(argv[4]),
            int(argv[5]),
            float(argv[6]),
            (int(argv[7]), int(argv[8])),
            float(argv[9]),
        )
    except:
        print("\n".join([
            "{} SEED N_COL N_ROW RESOLUTION OCTAVES PERSISTENCE PLOT_X PLOT_Y "
            "GRID_PLOT_PAD".format(argv[0]),
            "  SEED          : int   (,)",
            "  N_COL         : int   [2,)",
            "  N_ROW         : int   [2,)",
            "  RESOLUTION    : int   [2,)",
            "  OCTAVES       : int   [1,)",
            "  PERSISTENCE   : float [0.0,)",
            "  PLOT_X        : int   [1,)",
            "  PLOT_Y        : int   [1,)",
            "  GRID_PLOT_PAD : float [0.0,)",
        ]))
        exit(1)


def pad_axis(ax, xs, ys, k):
    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)
    x_pad = (x_max - x_min) * k
    y_pad = (y_max - y_min) * k
    pad = y_pad if x_pad < y_pad else x_pad
    ax.set_xlim([x_min - pad, x_max + pad])
    ax.set_ylim([y_min - pad, y_max + pad])


def export(filename):
    tight_layout()
    savefig(filename)
    close()


def plot_grid(
    xs,
    ys,
    vxs,
    vys,
    n,
    n_col,
    n_row,
    figsize,
    pad,
    filename,
):
    _, ax = subplots(figsize=figsize)
    kwargs = {"alpha": 0.75}
    for i in range(n_row):
        ax.plot([0, n_col - 1], [i, i], linestyle="--", zorder=0, **kwargs)
    for j in range(n_col):
        ax.plot([j, j], [0, n_row - 1], linestyle="--", zorder=0, **kwargs)
    ax.scatter(xs, ys, zorder=1, **kwargs)
    ax.scatter(xs + vxs, ys + vys, zorder=1, **kwargs)
    for ij in range(n):
        arrow(
            xs[ij],
            ys[ij],
            vxs[ij],
            vys[ij],
            head_width=0.075,
            length_includes_head=True,
            color="k",
            zorder=2,
            **kwargs,
        )
    pad_axis(ax, xs, ys, pad)
    ax.set_aspect("equal")
    export(filename)


def plot_noise(zs, figsize, filename):
    _, ax = subplots(figsize=figsize)
    ax.matshow(zs, cmap="bone")
    ax.invert_yaxis()
    export(filename)


def plot_map(zs, figsize, filename):
    cmap = ListedColormap([
        "#263878",
        "#324ca8",
        "#4362d1",
        "#dbc984",
        "wheat",
        "moccasin",
        "tan",
        "#a3855a",
        "forestgreen",
        "green",
        "darkgreen",
        "#17541a",
    ])
    norm = BoundaryNorm([
        0,
        0.315,
        0.43,
        0.5,
        0.525,
        0.55,
        0.61,
        0.65,
        0.7,
        0.7575,
        0.825,
        0.915,
        1,
    ], cmap.N, clip=True)
    _, ax = subplots(figsize=figsize)
    ax.matshow(zs, cmap=cmap, norm=norm)
    ax.invert_yaxis()
    export(filename)


def filepath(filename):
    return "{}/out/{}".format(WD, filename)


def timer(label, function, *args, **kwargs):
    t = time()
    x = function(*args, **kwargs)
    print("{:>24} : {:.5f}".format(label, time() - t))
    return x


def main():
    (s, n_col, n_row, resolution, octaves, persistence, figsize, pad) = \
        get_args()
    seed(s)
    n = n_col * n_row
    (xs, ys, vxs, vys) = timer("grid.init(...)", grid.init, n, n_col, n_row)
    timer(
        "main.plot_grid(...)",
        plot_grid,
        xs,
        ys,
        vxs,
        vys,
        n,
        n_col,
        n_row,
        figsize,
        pad,
        filepath("grid.png"),
    )
    (zs, res_n_col, res_n_row) = timer(
        "noise.iterate(...)",
        noise.iterate,
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
    )
    args = (noise.normalize(zs).reshape(res_n_row, res_n_col), figsize)
    timer(
        "main.plot_noise(...)",
        plot_noise,
        *args,
        filepath("noise.png"),
    )
    timer(
        "main.plot_map(...)",
        plot_map,
        *args,
        filepath("map.png"),
    )


if __name__ == "__main__":
    main()
