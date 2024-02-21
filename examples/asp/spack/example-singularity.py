import json
import os
import sys

from model import SpackGraphs

from compspec.asp import Difference

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)


def main():
    lib1 = os.path.join(here, "lib", "singularity", "singularity.json")
    lib2 = os.path.join(here, "lib", "singularity", "singularity-ce.json")

    for lib in lib1, lib2:
        if not os.path.exists(lib):
            sys.exit(f"{lib} does not exist.")

    # Run the diff! This is an iterative diff, meaning we are comparing subgraphs,
    # and have one top level graph that describes package relationships.

    A = SpackGraphs(lib1, "singularity")
    B = SpackGraphs(lib2, "singularity")
    for group, graph in A:
        if group in B:
            gA = A[group]
            gB = B[group]
            runner = Difference(gA, gB, "singularity", "singularity-ce", quiet=True)
            result = runner.run()
            if not result:
                continue
            print(f"Found result for group '{group}'")
            print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
