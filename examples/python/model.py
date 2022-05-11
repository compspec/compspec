__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

# This is the base model for deriving facts from ast in json

from compspec.utils import read_json
import compspec.graph
import compspec.solver


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
