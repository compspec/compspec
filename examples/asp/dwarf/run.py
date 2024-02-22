import json
import os
import sys

from compspec.asp import Difference

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)
from model import DwarfGraph


def main(name, lib1=None, lib2=None, groups=False):
    # Hard coded examples, for now
    lib1 = os.path.join(here, "lib", name, "v1", lib1 or "lib.v1.so")
    lib2 = os.path.join(here, "lib", name, "v2", lib2 or "lib.v2.so")

    for lib in lib1, lib2:
        if not os.path.exists(lib):
            sys.exit(f"{lib} does not exist.")

    # Create the two graphs, scope analysis to line program example.cpp
    # and optionally if there is a header.h
    A = DwarfGraph(lib1, ["example.cpp", "example.h"])
    B = DwarfGraph(lib2, ["example.cpp", "example.h"])

    runner = Difference(A, B, "A", "B", quiet=True)
    result = runner.run()

    # Groups help to organize output in GitHub workflows
    if groups:
        print(f"::group::{name}")
    print(json.dumps(result, indent=4))
    if groups:
        print("::endgroup::")
    return result, runner


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Please enter the name of an example (under lib) to run!")
    main(sys.argv[1])
