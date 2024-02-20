# This example shows generating subgraps on the level of functions

from model import AstFunctionGraphs, run

import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)


def main():
    lib1 = os.path.join(here, "lib", "tensorflow", "functiondb-2.7.0.json")
    lib2 = os.path.join(here, "lib", "tensorflow", "functiondb-2.6.2.json")

    for lib in lib1, lib2:
        if not os.path.exists(lib):
            sys.exit(f"{lib} does not exist.")

    run(lib1, lib2, AstFunctionGraphs)


if __name__ == "__main__":
    main()
