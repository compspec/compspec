# Python Module Changes

This is a fun example that will attempt to a diff between two different
Python modules. We do this using the [Caliper](https://github.com/vsoch/caliper)
library, which under the hood uses [Abstract Syntax Trees](https://docs.python.org/3/library/ast.html).
The two tensorflow files are derived from the "functiondb" (function database)
extractor, which has a small archive of results in [this repository](https://github.com/vsoch/caliper).
This provides another example of a kind of "diff" we can customize and run
relevant to code, interpreted and not compiled.

## Setup

First make sure you have compspec installed.

## Usage

This assumes you have a Python environment with compspec installed.

The first example shows breaking a large graph into subgraphs (e.g., on the level
of a function) and stopping as soon as we find an ABI break.

```bash
$ python tensorflow-module-example.py
```
```
Found result for group 'tensorflow.lite.python.wrap_toco'
{
    "removed_node": [
        [
            "A",
            "B",
            "id39",
            "function",
            "wrapped_retrieve_collected_errors",
            "module:tensorflow.lite.python.wrap_toco->function:wrapped_retrieve_collected_errors"
        ],
        [
            "A",
            "B",
            "id40",
            "function",
            "wrapped_flat_buffer_file_to_mlir",
            "module:tensorflow.lite.python.wrap_toco->function:wrapped_flat_buffer_file_to_mlir"
        ]
    ],
    "changed_node_value": [
        [
            "A",
            "B",
            "id29",
            "id29",
            "parameter",
            "denylisted_ops",
            "blocklisted_ops",
            "module:tensorflow.lite.python.wrap_toco->function:wrapped_experimental_mlir_quantize->parameter:denylisted_ops",
            "module:tensorflow.lite.python.wrap_toco->function:wrapped_experimental_mlir_quantize->parameter:blocklisted_ops"
        ],
        [
            "A",
            "B",
            "id31",
            "id31",
            "parameter",
            "denylisted_nodes",
            "blocklisted_nodes",
            "module:tensorflow.lite.python.wrap_toco->function:wrapped_experimental_mlir_quantize->parameter:denylisted_nodes",
            "module:tensorflow.lite.python.wrap_toco->function:wrapped_experimental_mlir_quantize->parameter:blocklisted_nodes"
        ]
    ]
}
Detected ABI break in subgraph, stopping.
```
The second one is similar to the above, but instead of looking on the level of
the module, we look on the level of functions within modules, and "flatten" the module
name to be an attribute of a function (sort of reversing the relationship).


```bash
$ python tensorflow-function-example.py
```

The second one is intended to show a more "obvious" way of doing it - creating
subgraphs based on different levels from the root. E.g.:

```
module tensorflow

  level 1: sub-modules
  level 2: functions
  level 3: parameters
```

And so for our first run, we only look at submodules (just called "modules" and iteratively
grow the graph as we increase the depth of our search. In practice this isn't ideal because
we may need to search the "lowest" levels, but doing so in this fashion is not computationally ideal.

```bash
$ python tensorflow-example.py
```

The second example creates subgraphs on the level of a particular attribute -
is this case the python function. We thus have many roots

