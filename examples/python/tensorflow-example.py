__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from compspec.runner import Difference
from model import AstGraphs

import os
import sys
import json

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)


def main():
    lib1 = os.path.join(here, "lib", "tensorflow", "functiondb-2.7.0.json")
    lib2 = os.path.join(here, "lib", "tensorflow", "functiondb-2.6.2.json")

    for lib in lib1, lib2:
        if not os.path.exists(lib):
            sys.exit(f"{lib} does not exist.")

    # Run the diff! The iterative diff is modeled slightly different -
    # we generate the graphs first and provide them to the runner
    # as the graphs need to be iterated over to provide groups to parse

    A = AstGraphs(lib1, "tensorflow")
    B = AstGraphs(lib2, "tensorflow")
    for group, graph in A:
        if group in B:
            gA = A[group]
            gB = B[group]
            print(f"Running for group '{group}'")
            runner = Difference(gA, gB, "A", "B", quiet=True)
            result = runner.run()
            print(f"Results for group '{group}'")
            print(json.dumps(result, indent=4))

            # Don't parse further nested, just a demo
            break


if __name__ == "__main__":
    main()
