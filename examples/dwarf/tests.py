#!/usr/bin/python

# Copyright (C) 2022 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import compspec.utils as utils
import pytest
import shutil
import sys
import os
import io

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)
from run import main as run

examples = utils.read_yaml("examples.yaml")
tests = []
for e in examples["examples"]:
    if "name" not in e:
        continue
    tests.append((e["name"], e.get("lib1", "lib.v1.so"), e.get("lib2", "lib.v2.so")))


@pytest.mark.parametrize("name,lib1,lib2", tests)
def test_examples(tmp_path, name, lib1, lib2):
    run(name, lib1, lib2)
