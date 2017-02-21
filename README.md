# Usage:
`./solomagic.py input.text [rules..]`

# Examples:
Without any rules it should output the same input file as is.
```
./solomagic.py input.text
```

As soon as we need rules we'll append them to the command line:
```
./solomagic.py input.text QtoApostrophe createMa
```

The output will correspond to the resulting file, which can be redirected as desired:
```
./solomagic.py input.text QtoApostrophe createMa > myawesomenewfile.text
```

# Testing
[![Build Status](https://travis-ci.org/aleixpol/solomagic.svg?branch=master)](https://travis-ci.org/aleixpol/solomagic)
Tests are triggered by `tests/test.py`, can conveniently be called by `make check`.

`*.in` files are input files and `*.out` are resulting files. To request new features, feel free to add more tests.
