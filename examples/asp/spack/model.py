__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

# This is the base model for deriving facts from ast in json

import compspec.graph
import compspec.solver
from compspec.utils import read_json


class SpackGraphs(compspec.graph.GraphGroup):
    """
    A namespace to hold more than one graph about spack.
    """

    def __init__(self, specfile, package):
        self.spec = read_json(specfile)["spec"]
        self.package = package
        super().__init__()

    def extract(self):
        """
        Extract named groups into different graphs
        """
        g = compspec.graph.Graph()
        root = g.new_node("spec", self.package)

        # First try one graph (we can create graphs for other things if needed)
        for spec in self.spec["nodes"]:
            # The version of the library
            node, _ = g.gen("spec", spec["name"], parent=root.nodeid)
            g.gen("version", spec["version"], parent=node.nodeid)
            g.gen("arch:platform", spec["arch"]["platform"], parent=node.nodeid)
            g.gen("arch:platform_os", spec["arch"]["platform_os"], parent=node.nodeid)

            # Flatten compiler and version, easy to see that difference
            target = spec["arch"]["target"]
            if isinstance(target, dict):
                target = target["vendor"] + " " + target["name"]
            g.gen("arch:target", target, parent=node.nodeid)
            g.gen(
                "compiler",
                spec["compiler"]["name"] + "@" + spec["compiler"]["version"],
                parent=node.nodeid,
            )
            g.gen("namespace", spec["namespace"], parent=node.nodeid)

            # I think this is DAG hash, keep this one
            g.gen("hash", spec["hash"], parent=node.nodeid)

            for paramname, value in spec["parameters"].items():
                if paramname == "patches":
                    value = len(value)
                if value in [True, False] or (isinstance(value, list) and value):
                    g.gen(paramname, value, parent=node.nodeid)

            for dep in spec.get("dependencies", []):
                depnode, _ = g.gen("dependency", dep["name"], parent=node.nodeid)
                g.gen("dephash", dep["build_hash"], parent=depnode.nodeid)
                types = dep["type"]
                types.sort()
                types = "|".join(types)
                g.gen("deptypes", types, parent=depnode.nodeid)

        # Save the named graph
        self.graphs[self.package] = g
