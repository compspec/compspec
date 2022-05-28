__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

# This is the base model for deriving facts from ast in json

from deid.dicom.parser import DicomParser
import compspec.graph
import compspec.solver
import nibabel


class DicomGraphs(compspec.graph.GraphGroup):
    """
    A namespace to hold more than one graph about dicom files.
    """

    def __init__(self, dcm, ns):
        self.dcm = DicomParser(dcm)
        self.dcm.parse()
        self.ns = ns
        super().__init__()

    def extract(self):
        """
        Extract named groups into different graphs
        """
        # First try just the header
        g = compspec.graph.Graph()
        root = g.new_node("header", self.ns)

        for name, field in self.dcm.fields.items():
            f, _ = g.gen("field", name, parent=root.nodeid)
            n, _ = g.gen("field-name", field.name, parent=f.nodeid)
            g.gen("field-value", field.element.value, parent=n.nodeid)

        # Save the named graph - the header is tested first so we can stop
        # if there are differences.
        self.graphs["header"] = g
