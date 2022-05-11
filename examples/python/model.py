__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

# This is the base model for deriving facts from ast in json

from compspec.runner import Difference
from compspec.utils import read_json
import compspec.graph
import compspec.solver
import json


class AstGraphs(compspec.graph.GraphGroup):
    """
    A namespace to hold more than one graph (can this be generalized?)
    """

    def __init__(self, lib, module_name):
        self.ast = read_json(lib)
        self.module_name = module_name
        super().__init__()

    def extract(self):
        """
        Extract named groups into different graphs
        """
        # We should have only one version!
        assert len(self.ast) == 1
        version = list(self.ast.keys())[0]

        # Initialize groups
        groups = ["module", "function", "parameter"]

        # Create a graph for each group
        for group in groups:

            g = compspec.graph.Graph()

            # Create the root of the library (single root)
            root = g.new_node("module", self.module_name)

            # The version of the library
            g.gen("version", version, parent=root.nodeid)

            for submod_name, items in self.ast[version].items():
                submod, _ = g.gen("module", submod_name, parent=root.nodeid)

                # Module graph doesn't include anything else
                if group == "module":
                    continue

                for funcname, params in items.items():
                    func, _ = g.gen("function", funcname, parent=submod.nodeid)
                    if group == "function":
                        continue

                    for order, param in enumerate(params):
                        g.gen("parameter", param, parent=func.nodeid)
                        g.gen("order", order, parent=func.nodeid)

            # Save the named graph
            self.graphs[group] = g


class AstModuleGraphs(AstGraphs):
    """
    A second example that generates "roots" on the level of the module.
    """

    def extract(self):
        """
        Extract named groups into different graphs
        """
        # We should have only one version!
        assert len(self.ast) == 1
        version = list(self.ast.keys())[0]

        # Each module will be a root
        for submod_name, items in self.ast[version].items():

            # Create a new graph
            g = compspec.graph.Graph()

            # The module is the quasi root
            submod = g.new_node("module", submod_name)

            for funcname, params in items.items():
                func, _ = g.gen("function", funcname, parent=submod.nodeid)
                for order, param in enumerate(params):
                    g.gen("parameter", param, parent=func.nodeid)
                    g.gen("order", order, parent=func.nodeid)

            # Save the named graph
            self.graphs[submod_name] = g


class AstFunctionGraphs(AstGraphs):
    """
    A third example that generates "roots" on the level of the function.
    """

    def extract(self):
        """
        Extract named groups into different graphs
        """
        # We should have only one version!
        assert len(self.ast) == 1
        version = list(self.ast.keys())[0]

        # Each module will be a root
        for submod_name, items in self.ast[version].items():

            # Create a new graph
            g = compspec.graph.Graph()

            # The module will be added as an attribute
            module = g.new_node("module", submod_name)

            for funcname, params in items.items():

                root = g.new_node("function", funcname)
                g.new_relation(root, "has", module)
                for order, param in enumerate(params):
                    g.gen("parameter", param, parent=root.nodeid)
                    g.gen("order", order, parent=root.nodeid)

                # Save the named graph
                self.graphs[funcname] = g


def run(lib1, lib2, GraphClass=AstGraphs):
    """
    Shared run function to run with some particular class name.
    """
    # Run the diff! The iterative diff is modeled slightly different -
    # we generate the graphs first and provide them to the runner
    # as the graphs need to be iterated over to provide groups to parse

    A = GraphClass(lib1, "tensorflow")
    B = GraphClass(lib2, "tensorflow")
    for group, graph in A:
        if group in B:
            gA = A[group]
            gB = B[group]
            runner = Difference(gA, gB, "A", "B", quiet=True)
            result = runner.run()
            if not result:
                continue
            print(f"Found result for group '{group}'")
            print(json.dumps(result, indent=4))

            # We can stop as soon as we have results that are missing
            if (
                "removed_node" in result
                or "added_node" in result
                or "changed_node_value" in result
            ):
                # We are interested in changes TO a                
                print("Detected ABI break in subgraph, stopping.")
                break
