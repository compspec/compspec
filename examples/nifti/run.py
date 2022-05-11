__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from compspec.runner import Difference
from model import NiftiGraphs

import os
import sys
import json

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)


def main():
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
            runner = Difference(gA, gB, "zeros", "modified", quiet=False)
            result = runner.run()
            print(f"Result for group '{group}'")
            print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
