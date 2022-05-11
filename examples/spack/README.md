# Spack Changes

This is a quick example to show how to do a diff between spack specs!

## Usage

This assumes you have a Python environment with compspec installed.


```bash
$ python example-singularity.py
```
```
Found result for group 'singularity'
{
    "changed_node_value": [
        [
            "singularity",
            "singularity-ce",
            "id1",
            "id1",
            "spec",
            "singularity",
            "singularityce",
            "spec:singularity->spec:singularity",
            "spec:singularity->spec:singularityce"
        ],
        [
            "singularity",
            "singularity-ce",
            "id2",
            "id2",
            "version",
            "3.8.5",
            "3.9.1",
            "spec:singularity->spec:singularity->version:3.8.5",
            "spec:singularity->spec:singularityce->version:3.9.1"
        ],
        [
            "singularity",
            "singularity-ce",
            "id8",
            "id8",
            "hash",
            "7xywcuaorwa6pt3bcct6ptc3p7j3rqtm",
            "3ps6gdd3tydgvrxj6onz7qyj3osbs5p2",
            "spec:singularity->spec:singularity->hash:7xywcuaorwa6pt3bcct6ptc3p7j3rqtm",
            "spec:singularity->spec:singularityce->hash:3ps6gdd3tydgvrxj6onz7qyj3osbs5p2"
        ]
    ]
}
```
That's not super interesting, because the only changes are between the name, version,
and hashes. Try running Python for a more verbose result.


```bash
$ python example-python.py
```

