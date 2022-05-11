# Python Dwarf Changes

This example shows using the compspec Difference class to create a custom
class to inspect changes in DWARF, which is the debugging format for a binary (ELF).
Conceptually we are:

1. Creating two graphs that include dwarf
2. Running them through the difference model

and that's it!

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
And then run the examples! The libmath shows a table output:


```bash
$ python libmath-example.py
```

| Name | Value | Change Type | A | B | Description |
|------|-------|-------------|---|---|-------------|
|function|_ZN11MathLibrary10Arithmetic3AddEdd -> _ZN11MathLibrary10Arithmetic3AddEii|change|A|B|compileunit:MathLibrary.cpp->namespace:MathLibrary->class:Arithmetic->function:_ZN11MathLibrary10Arithmetic3AddEdd -> compileunit:MathLibrary.cpp->namespace:MathLibrary->class:Arithmetic->function:_ZN11MathLibrary10Arithmetic3AddEii|
|type|double -> int|change|A|B|compileunit:MathLibrary.cpp->namespace:MathLibrary->class:Arithmetic->function:_ZN11MathLibrary10Arithmetic3AddEdd->type:double -> compileunit:MathLibrary.cpp->namespace:MathLibrary->class:Arithmetic->function:_ZN11MathLibrary10Arithmetic3AddEii->type:int|
|type|double -> int|change|A|B|compileunit:MathLibrary.cpp->namespace:MathLibrary->class:Arithmetic->function:_ZN11MathLibrary10Arithmetic3AddEdd->parameter:unknown->type:double -> compileunit:MathLibrary.cpp->namespace:MathLibrary->class:Arithmetic->function:_ZN11MathLibrary10Arithmetic3AddEii->parameter:unknown->type:int|
|type|double -> int|change|A|B|compileunit:MathLibrary.cpp->namespace:MathLibrary->class:Arithmetic->function:_ZN11MathLibrary10Arithmetic3AddEdd->parameter:unknown->type:double -> compileunit:MathLibrary.cpp->namespace:MathLibrary->class:Arithmetic->function:_ZN11MathLibrary10Arithmetic3AddEii->parameter:unknown->type:int|
|basetype|double -> int|change|A|B|compileunit:MathLibrary.cpp->basetype:double -> compileunit:MathLibrary.cpp->basetype:int|
|size|8 -> 4|change|A|B|compileunit:MathLibrary.cpp->basetype:double->size:8 -> compileunit:MathLibrary.cpp->basetype:int->size:4|
|location|framebase-20|add|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:a->location:framebase-20|
|function||remove|A|B|compileunit:MathLibrary.cpp->function:unknown|
|location||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:a->location:framebase-24|
|size||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:b->size:0|
|location||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:b->location:framebase-32|
|location||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:a->location:framebase-24|
|size||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:b->size:0|
|location||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:b->location:framebase-32|
|location||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:a->location:framebase-24|
|size||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:b->size:0|
|location||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:b->location:framebase-32|
|location||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:a->location:framebase-24|
|size||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:b->size:0|
|location||remove|A|B|compileunit:MathLibrary.cpp->function:unknown->parameter:b->location:framebase-32|

And try running for an array:

```bash
$ python array-example.py
```
```bash
{
    "changed_node_value": [
        [
            "A",
            "B",
            "id3",
            "id3",
            "size",
            "36",
            "104",
            "compileunit:array.cpp->structure:Foo->size:36",
            "compileunit:array.cpp->structure:Foo->size:104"
        ],
        [
            "A",
            "B",
            "id14",
            "id14",
            "count",
            "31",
            "99",
            "compileunit:array.cpp->array:unknown->subrange:unknown->count:31",
            "compileunit:array.cpp->array:unknown->subrange:unknown->count:99"
        ]
    ]
}
```

Or an inline function:

```bash
$ python callsite-example.py
```
```
{
    "changed_node_value": [
        [
            "A",
            "B",
            "id52",
            "id52",
            "function",
            "inline_this",
            "inline_that",
            "compileunit:callsite.cpp->function:inline_this",
            "compileunit:callsite.cpp->function:inline_that"
        ]
    ]
}
```

**more coming soon!** @vsoch will be adding more simple examples to parse different
DWARF information entries.
