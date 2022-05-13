# Python Dwarf Changes

This set of examples shows using the compspec Difference class to create a custom
class to inspect changes in DWARF, which is the debugging format for a binary (ELF).
Conceptually we are:

1. Creating two graphs that include dwarf
2. Running them through the difference model

and that's it!

## Structure

The examples are strucutred as follows:

1. Each subfolder in [libs](lib) represents a single type of change, and has a `v1` and `v2` file, each with:
  a. example.cpp
  b. builds to lib.v1.so or lib.v2.so
  c. a Makefile
2. The compilation and testing can be done with [tests.py](tests.py)
3. Each test looks for a particular kind of change.

Here is an example for "array":

```
$ tree array/
array/
├── v1
│   ├── example.cpp
│   ├── lib.v1.so
│   └── Makefile
└── v2
    ├── example.cpp
    ├── lib.v2.so
    └── Makefile

2 directories, 6 files
```

This means if you want to add a new lib (example and test) just:

1. Create a new directory under [lib](lib) with this structure
2. Add an entry to [examples.yaml](examples.yaml)
3. Compile with `make`
4. Test!

```bash
$ make
$ pytest tests.py
```

## Setup

Examples for different kinds of C++ libraries are provided in [lib], and all can 
first be built with the [Makefile](Makefile):

```bash
make
```

And make sure you have complib installed, along with the additional depdendency
pyelftools:

```bash
$ pip install -r requirements.txt
```

These libraries will be required for the examples, so make sure you have them!

## Usage

This assumes you have a Python environment with compspec installed.
You can use [run.py](run.py) to run any specific example, which is a named
directory under [lib](lib). For example:


```bash
$ python run.py libmath
```

## Questions

1. Why does libmath generate subprogrms without names with callsite flag attributes?
