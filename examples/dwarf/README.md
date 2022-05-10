# Python Dwarf Changes

This example shows using the compspec Difference class to create a custom
class to inspect changes in DWARF, which is the debugging format for a binary (ELF).

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
And then run the examples!

```bash
$ python libmath-example.py
```

**more coming soon!** @vsoch will be adding more simple examples to parse different
DWARF information entries.
