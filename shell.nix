with import <nixpkgs> {};
mkShell {
    buildInputs = [
        (python38.withPackages(ps: with ps; [
            flake8
            matplotlib
            numba
            numpy
            setuptools
        ]))
        shellcheck
    ];
    shellHook = ''
        . .shellhook
    '';
}
