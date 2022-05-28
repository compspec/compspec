# Dicom Changes

This is a quick example to show how to do a diff between dicom headers.

## Usage

This assumes you have a Python environment with compspec installed.
Install deid:

```bash
pip install -r requirements.txt
```

And then run the example

```bash
$ python run.py
```
```
Result for image1.dcm vs. image4.dcm group 'header'
{
    "changed_node_value": [
        [
            "A",
            "B",
            "id12",
            "id12",
            "field-value",
            "F",
            "M",
            "header:image->field:(0010, 0040)->field-name:PatientSex->field-value:F",
            "header:image->field:(0010, 0040)->field-name:PatientSex->field-value:M"
        ]
    ]
}
Result for image4.dcm vs. image1.dcm group 'header'
{
    "changed_node_value": [
        [
            "A",
            "B",
            "id12",
            "id12",
            "field-value",
            "M",
            "F",
            "header:image->field:(0010, 0040)->field-name:PatientSex->field-value:M",
            "header:image->field:(0010, 0040)->field-name:PatientSex->field-value:F"
        ]
    ]
}
```
