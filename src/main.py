#!/usr/bin/env python3

from os import environ
from random import seed
from time import time

from matplotlib.pyplot import arrow, close, savefig, subplots, tight_layout
from numpy import max, min

from grid import init, N, N_COL, N_ROW
from noise import iterate, RES_N_COL, RES_N_ROW

WD = environ["WD"]
SEED = 1
FIGSIZE = (15, 12)
PAD = 0.1


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


def plot_grid(xs, ys, cxs, cys, filename):
    _, ax = subplots(figsize=FIGSIZE)
    kwargs = {"alpha": 0.75}
    for i in range(N_ROW):
        ax.plot([0, N_COL - 1], [i, i], linestyle="--", zorder=0, **kwargs)
    for j in range(N_COL):
        ax.plot([j, j], [0, N_ROW - 1], linestyle="--", zorder=0, **kwargs)
    ax.scatter(xs, ys, zorder=1, **kwargs)
    ax.scatter(xs + cxs, ys + cys, zorder=1, **kwargs)
    for ij in range(N):
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
    pad_axis(ax, xs, ys, PAD)
    ax.set_aspect("equal")
    tight_layout()
    savefig(filename)
    close()


def plot_noise(zs, filename):
    _, ax = subplots(figsize=FIGSIZE)
    ax.matshow(zs, cmap="Greys")
    ax.invert_yaxis()
    tight_layout()
    savefig(filename)
    close()


def filepath(filename):
    return "{}/out/{}".format(WD, filename)


def timer(f, label):
    t = time()
    x = f()
    print("{:>18} : {:.5f}".format(label, time() - t))
    return x


def main():
    seed(SEED)
    (xs, ys, cxs, cys) = timer(init, "init()")
    zs = timer(lambda: iterate(xs, ys, cxs, cys), "noise(...)")
    timer(lambda: plot_grid(
        xs,
        ys,
        cxs,
        cys,
        filepath("grid.png"),
    ), "plot_grid(...)")
    timer(lambda: plot_noise(
        zs.reshape(RES_N_ROW, RES_N_COL),
        filepath("noise.png"),
    ), "plot_noise(...)")


if __name__ == "__main__":
    main()
