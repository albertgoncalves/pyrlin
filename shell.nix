with import <nixpkgs> {};
mkShell {
    buildInputs = [
        (python37.withPackages(ps: with ps; [
            flake8
            matplotlib
            numba
            numpy
        ]))
    ];
    shellHook = ''
        . .shellhook
    '';
}
