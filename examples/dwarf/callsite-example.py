__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from model import DwarfDifference

import os
import sys
import json

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)


def main():
    # Hard coded examples, for now
    lib1 = os.path.join(here, "lib", "callsite", "v1", "libcallsite.v1.so")
    lib2 = os.path.join(here, "lib", "callsite", "v2", "libcallsite.v2.so")

    for lib in lib1, lib2:
        if not os.path.exists(lib):
            sys.exit(f"{lib} does not exist.")

    # Run the diff!
    runner = DwarfDifference(lib1, lib2)
    result = runner.run()
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
