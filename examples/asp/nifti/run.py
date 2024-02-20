from compspec.asp import Difference
from model import NiftiGraphs

import os
import sys
import json

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)


def main():
    """
    The truth (changed values) is:

    x  y  z  zeros modified
    16 16 5  0.0   1.0
    32 32 10 0.0   1e-09
    35 15 7  0.0   3.0
    50 50 15 0.0   2.0
    """
    nii1 = os.path.join(here, "lib", "zeros.nii")
    nii2 = os.path.join(here, "lib", "modified.nii")

    for nii in nii1, nii2:
        if not os.path.exists(nii):
            sys.exit(f"{nii} does not exist.")

    # Run the diff! This is an iterative diff, meaning we are comparing subgraphs,
    # and have one top level graph that describes package relationships.
    A = NiftiGraphs(nii1, "brain")
    B = NiftiGraphs(nii2, "brain")
    for group, graph in A:
        if group in B:
            gA = A[group]
            gB = B[group]
            if group == "header":
                runner = Difference(gA, gB, "zeros", "modified", quiet=True)
                result = runner.run()
            # Omit default logic program for image data
            else:
                runner = Difference(gA, gB, "zeros", "modified", quiet=True)
                result = runner.run(
                    logic_programs=["compare-voxels.lp"], omit_default=True
                )
            print(f"Result for group '{group}'")
            print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
