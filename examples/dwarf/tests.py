#!/usr/bin/python

# Copyright (C) 2022 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import compspec.utils as utils
import pytest
import json
import shutil
import sys
import os
import io

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)
from run import main as run

# Custom names or libs
examples = utils.read_yaml("examples.yaml")
tests = []
seen = set()
for e in examples["examples"]:
    if "name" not in e:
        continue
    tests.append((e["name"], e.get("lib1", "lib.v1.so"), e.get("lib2", "lib.v2.so")))
    seen.add(e["name"])

# Add remainder
for name in os.listdir(os.path.join(here, "lib")):
    if name not in seen:
        tests.append((name, "lib.v1.so", "lib.v2.so"))
    seen.add(name)


def check_facts(facts, graph):

    # Just check nodes for now
    expected = utils.read_json(facts)
    for n in expected.get("nodes", []):
        assert n["nodeid"] in graph.nodes
        node = graph.nodes[n["nodeid"]]
        assert node.name == n["name"]
        assert node.value == n["value"]

    # TODO check relations?


@pytest.mark.parametrize("name,lib1,lib2", tests)
def test_examples(tmp_path, name, lib1, lib2):
    result, runner = run(name, lib1, lib2, groups=True)

    # Do we have a facts file to validate?
    facts_A = os.path.join(here, "lib", name, "A.json")
    facts_B = os.path.join(here, "lib", name, "B.json")

    # Check facts (nodes and relations)
    if os.path.exists(facts_A):
        check_facts(facts_A, runner.facts.A)
    else:
        utils.write_json(runner.facts.A.to_dict(), facts_A)
    if os.path.exists(facts_B):
        check_facts(facts_B, runner.facts.B)
    else:
        utils.write_json(runner.facts.B.to_dict(), facts_B)

    # Compare with our expected results
    expected = os.path.join(here, "lib", name, "compspec.json")
    if os.path.exists(expected):
        expected = utils.read_json(expected)

        # Check top level keys
        for key in result:
            assert key in expected

        # First check everything in result is in expected
        for key, values in result.items():

            # and list entries
            for value in values:
                if value not in expected[key]:
                    sys.exit(
                        "Found unexpected %s value:\n%s"
                        % (key, json.dumps(value, indent=4))
                    )

        # And everything in expected is in result
        for key, values in expected.items():

            # and list entries
            for value in values:
                if value not in result[key]:
                    sys.exit(
                        "Missing %s value:\n%s" % (key, json.dumps(value, indent=4))
                    )
