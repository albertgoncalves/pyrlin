#!/usr/bin/env python3

from os import environ
from random import seed
from time import time
from sys import argv

from matplotlib.pyplot import arrow, close, savefig, subplots, tight_layout
from numpy import max, min

from grid import init
from noise import iterate

WD = environ["WD"]


def args():
    try:
        return (
            int(argv[1]),
            int(argv[2]),
            int(argv[3]),
            int(argv[4]),
            int(argv[5]),
            int(argv[6]),
            float(argv[7]),
        )
    except:
        print(" ".join([
            "$ {} <seed: int> <n_col: int> <n_row: int>".format(argv[0]),
            "<res: int> <fig_x: int> <fig_y: int> <fig_pad: float>",
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


def plot_grid(
    xs,
    ys,
    cxs,
    cys,
    n,
    n_col,
    n_row,
    fig_x,
    fig_y,
    fig_pad,
    filename,
):
    _, ax = subplots(figsize=(fig_x, fig_y))
    kwargs = {"alpha": 0.75}
    for i in range(n_row):
        ax.plot([0, n_col - 1], [i, i], linestyle="--", zorder=0, **kwargs)
    for j in range(n_col):
        ax.plot([j, j], [0, n_row - 1], linestyle="--", zorder=0, **kwargs)
    ax.scatter(xs, ys, zorder=1, **kwargs)
    ax.scatter(xs + cxs, ys + cys, zorder=1, **kwargs)
    for ij in range(n):
        arrow(
            xs[ij],
            ys[ij],
            cxs[ij],
            cys[ij],
            head_width=0.075,
            length_includes_head=True,
            color="k",
            zorder=2,
            **kwargs,
        )
    pad_axis(ax, xs, ys, fig_pad)
    ax.set_aspect("equal")
    tight_layout()
    savefig(filename)
    close()


def plot_noise(zs, fig_x, fig_y, filename):
    _, ax = subplots(figsize=(fig_x, fig_y))
    ax.matshow(zs, cmap="Greys")
    ax.invert_yaxis()
    tight_layout()
    savefig(filename)
    close()


def filepath(filename):
    return "{}/out/{}".format(WD, filename)


def timer(label, function, *args, **kwargs):
    t = time()
    x = function(*args, **kwargs)
    print("{:>24} : {:.5f}".format(label, time() - t))
    return x


def main():
    (s, n_col, n_row, res, fig_x, fig_y, fig_pad) = args()
    seed(s)
    n = n_col * n_row
    (xs, ys, vxs, vys) = timer("grid.init(...)", init, n, n_col, n_row)
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
        fig_x,
        fig_y,
        fig_pad,
        filepath("grid.png"),
    )
    (zs, res_n_col, res_n_row) = timer(
        "noise.iterate(...)",
        iterate,
        xs,
        ys,
        vxs,
        vys,
        n_col,
        n_row,
        res,
    )
    timer(
        "main.plot_noise(...)",
        plot_noise,
        zs.reshape(res_n_row, res_n_col),
        fig_x,
        fig_y,
        filepath("noise.png"),
    )


if __name__ == "__main__":
    main()
