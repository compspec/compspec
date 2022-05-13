__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from compspec.runner import Difference

import os
import sys
import json
import yaml

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)
from model import DwarfGraph


def main(name, lib1=None, lib2=None):

    # Hard coded examples, for now
    lib1 = os.path.join(here, "lib", name, "v1", lib1 or "lib.v1.so")
    lib2 = os.path.join(here, "lib", name, "v2", lib2 or "lib.v2.so")

    for lib in lib1, lib2:
        if not os.path.exists(lib):
            sys.exit(f"{lib} does not exist.")

    # Create the two graphs
    A = DwarfGraph(lib1)
    B = DwarfGraph(lib2)

    runner = Difference(A, B, "A", "B", quiet=True)
    result = runner.run()
    print(json.dumps(result, indent=4))
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Please enter the name of an example (under lib) to run!")
    main(sys.argv[1])
