# Python Dwarf Changes

This set of examples shows using the compspec Difference class to create a custom
class to inspect changes in DWARF, which is the debugging format for a binary (ELF).
Conceptually we are:

1. Creating two graphs that include dwarf
2. Running them through the difference model

and that's it! We are also trying to capture a list of basic tests that represent
ABI changes, including:

 - [lib/libmath](lib/libmath): A C++ function parameter type is changed
 - [lib/callsite](lib/callsite): A function used as a callsite is renamed
 - [lib/classinheritance](lib/classinheritance): An inherited class ordering is changed
 - [lib/classorder](lib/classorder): Order of classes provided to function are flipped.
 - [lib/function-params](lib/function-params): changed function parameters.
 - [lib/struct-change](lib/struct-change): A type is changed in a struct (same order and name)
 - [lib/struct-add](lib/struct-add): A field is added to a struct
 - [lib/struct-remove](lib/struct-remove): A field is removed a struct

Note that you should have `c++filt` on your system to demangle names.
Yes, it's kind of rough / hacky but we could always write this in a different
language if absolutely necessary.

**More coming soon!** If you have an example you want me to implemenent [please let me know](https://github.com/compspec/compspec/issuess).

Examples to add include:

 - cycle-handling
 - changing a named struct to anonymous
 - changing an anonymous struct to named
 - changing a named union to anonymous
 - changing an anonymous union to named
 - changing a named enum to anonymous
 - changing an anonymous enum to named (should report name change and member diffs)
 - struct with all possible C base types to test what names get generated
 - struct with all possible C++ base types to test what names get generated
 - variadic function types
 - struct containing members with types composed from chains of qualifiers and typedefs (with anarray of pointers at the base)
 - order of base classes in inheritance
 - qualifiers on member functions, access, namespaces
 - static data member is added or removed OR a static data member type size changed
 - if a data member is replaced by an anonymous data member
 - enum has insertion

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
4. Run once to get an expected result and save directly under the named directory as compspec.json
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
