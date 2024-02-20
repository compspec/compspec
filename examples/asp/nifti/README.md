# Nifti Changes

This is a quick example to show how to do a diff between nifti (dummy) brain maps.

## Usage

This assumes you have a Python environment with compspec installed.
Install nibabal:

```bash
pip install -r requirements.txt
```

And then run the example! Note that since clingo cannot support float, we arbitrarily multiply by 100
to convert to int and then we can subtract.

```bash
$ python run.py
```
```bash
esult for group 'header'
{}
Result for group 'image'
{
    "different_values": [
        [
            "modified",
            "zeros",
            "100",
            "0"
        ],
        [
            "modified",
            "zeros",
            "300",
            "0"
        ],
        [
            "modified",
            "zeros",
            "200",
            "0"
        ],
        [
            "zeros",
            "modified",
            "0",
            "100"
        ],
        [
            "zeros",
            "modified",
            "0",
            "300"
        ],
        [
            "zeros",
            "modified",
            "0",
            "200"
        ]
    ],
    "too_different": [
        [
            "modified",
            "zeros",
            "100",
            "0"
        ],
        [
            "modified",
            "zeros",
            "300",
            "0"
        ],
        [
            "modified",
            "zeros",
            "200",
            "0"
        ]
    ]
```
