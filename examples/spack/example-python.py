__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from compspec.runner import Difference
from model import SpackGraphs

import os
import sys
import json

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)


def main():
    lib1 = os.path.join(here, "lib", "python", "python2.7.json")
    lib2 = os.path.join(here, "lib", "python", "python3.8.json")

    for lib in lib1, lib2:
        if not os.path.exists(lib):
            sys.exit(f"{lib} does not exist.")

    # Run the diff! This is an iterative diff, meaning we are comparing subgraphs,
    # and have one top level graph that describes package relationships.

    A = SpackGraphs(lib1, "python")
    B = SpackGraphs(lib2, "python")
    for group, graph in A:
        if group in B:
            gA = A[group]
            gB = B[group]
            runner = Difference(gA, gB, "python2.7", "python3.8", quiet=True)
            result = runner.run()
            if not result:
                continue
            print(f"Found result for group '{group}'")
            print(json.dumps(result, indent=4))
            out = Difference.table(result)
            print(out)


if __name__ == "__main__":
    main()
