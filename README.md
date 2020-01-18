# pyrlin

| `grid`              | `noise`              | `map`              |
|:-------------------:|:--------------------:|:------------------:|
| ![](cover/grid.png) | ![](cover/noise.png) | ![](cover/map.png) |

Needed things
---
*   [Nix](https://nixos.org/nix/)

Quick start
---
```
$ nix-shell
[nix-shell:path/to/pyrlin]$ python src/main.py 99 5 5 1000 6 0.465 4 4 0.25
[nix-shell:path/to/pyrlin]$ open out/grid.png
[nix-shell:path/to/pyrlin]$ open out/noise.png
[nix-shell:path/to/pyrlin]$ open out/map.png
```

Args
---
```
src/main.py SEED N_COL N_ROW RESOLUTION OCTAVES PERSISTENCE PLOT_X PLOT_Y GRID_PLOT_PAD
  SEED          : int   (,)     <- random seed
  N_COL         : int   [2,)    <- number of grid columns
  N_ROW         : int   [2,)    <- number of grid rows
  RESOLUTION    : int   [2,)    <- interpolation resolution
  OCTAVES       : int   [1,)    <- number of octaves
  PERSISTENCE   : float [0.0,)  <- octave rate of decay
  PLOT_X        : int   [1,)    <- width of plots
  PLOT_Y        : int   [1,)    <- height of plots
  GRID_PLOT_PAD : float [0.0,)  <- grid plot axis padding
```

Helpful links
---
*   https://en.wikipedia.org/wiki/Perlin_noise
*   https://longwelwind.net/2017/02/09/perlin-noise.html
*   https://rmarcus.info/blog/2018/03/04/perlin-noise.html
*   https://flafla2.github.io/2014/08/09/perlinnoise.html
