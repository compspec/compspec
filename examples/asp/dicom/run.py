from compspec.asp import Difference
from model import DicomGraphs

import os
import sys
import json

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)


def main():
    dicom_dir = os.path.join(here, "lib")
    dicoms = os.listdir(dicom_dir)
    graphs = {}
    for dcm in dicoms:
        dcm_file = os.path.join(dicom_dir, dcm)
        if not os.path.exists(dcm_file):
            sys.exit(f"{dcm_file} does not exist.")
        graphs[dcm] = DicomGraphs(dcm_file, "image")

    # Run the diff! This is an iterative diff, meaning we are comparing subgraphs
    for nameA, A in graphs.items():
        for nameB, B in graphs.items():
            if nameA == nameB:
                continue
            for group, graph in A:
                if group in B:
                    gA = A[group]
                    gB = B[group]
                    runner = Difference(gA, gB, "A", "B", quiet=True)
                    result = runner.run()
                    print(f"Result for {nameA} vs. {nameB} group '{group}'")
                    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
