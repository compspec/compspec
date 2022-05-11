# Python Module Changes

This is a fun example that will attempt to a diff between two different
Python modules. We do this using the [Caliper](https://github.com/vsoch/caliper)
library, which under the hood uses [Abstract Syntax Trees](https://docs.python.org/3/library/ast.html).
The two tensorflow files are derived from the "functiondb" (function database)
extractor, which has a small archive of results in [this repository](https://github.com/vsoch/caliper).
This provides another example of a kind of "diff" we can customize and run
relevant to code, interpreted and not compiled.

## Setup

First make sure you have complib installed.

## Usage

This assumes you have a Python environment with compspec installed.
And then run the examples!

```bash
$ python tensorflow-example.py
```
```bash
(env) vanessa@vanessa-ThinkPad-T490s:~/Desktop/Code/compspec/compspec-python/examples/python$ python tensorflow-example.py 
Running for group module
Results for group module
{
    "is_a": [
        [
            "A"
        ]
    ],
    "is_b": [
        [
            "B"
        ]
    ],
    "is_different": [
        [
            "A",
            "B"
        ]
    ],
    "removed_node": [
        [
            "A",
            "B",
            "version",
            "2.6.2"
        ]
    ],
    "added_node": [
        [
            "A",
            "B",
            "version",
            "2.7.0"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.core.framework.dataset_metadata_pb2"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.core.protobuf.data_service_pb2"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.core.protobuf.status_pb2"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.lite.python.analyzer"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.lite.python.authoring"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.lite.python.authoring.authoring"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.lite.tools.flatbuffer_utils"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.lite.tools.optimize"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.lite.tools.optimize.debugging"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.lite.tools.optimize.debugging.python"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.lite.tools.optimize.debugging.python.debugger"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.data.ops.options"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.data.experimental.ops.random_access"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.data.experimental.kernel_tests.service.multi_process_cluster"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.util.traceback_utils"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.util.type_annotations"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.saved_model.registration"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.kernel_tests.sparse_xent_op_test_base"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.training.tracking.base_delegate"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.distribute.experimental.rpc"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.distribute.experimental.rpc.rpc_ops"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.python.distribute.coordinator.coordinator_context"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow._api.v2.compat.v1.lite.experimental.authoring"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow._api.v2.compat.v1.nn.experimental"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow._api.v2.compat.v2.lite.experimental.authoring"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow._api.v2.compat.v2.nn.experimental"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow._api.v2.compat.v2.distribute.experimental.rpc"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow._api.v2.lite.experimental.authoring"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow._api.v2.nn.experimental"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow._api.v2.distribute.experimental.rpc"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.distribute"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.distribute.experimental"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.distribute.experimental.rpc"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.distribute.experimental.rpc.proto"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.distribute.experimental.rpc.proto.tf_rpc_service_pb2"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.distribute.experimental.rpc.proto.tf_rpc_service_pb2_grpc"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.distribute.experimental.rpc.kernels.gen_rpc_ops"
        ],
        [
            "A",
            "B",
            "module",
            "tensorflow.distribute.experimental.rpc.kernels"
        ]
    ]
}
```
Note that for this example we only look at module level comparison (and not parameters) as
it would take much longer. This is done in an iterative approach to generate groups,
and I'm still wondering if we can further improve upon that.
