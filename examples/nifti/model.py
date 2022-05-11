__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

# This is the base model for deriving facts from ast in json

import compspec.graph
import compspec.solver
import nibabel


class NiftiGraphs(compspec.graph.GraphGroup):
    """
    A namespace to hold more than one graph about nifti files.
    """

    def __init__(self, nii, ns):
        self.nii = nibabel.load(nii)
        self.ns = ns
        super().__init__()

    def extract(self):
        """
        Extract named groups into different graphs
        """
        # First try just the header
        g = compspec.graph.Graph()
        root = g.new_node("brainmap", self.ns)

        for k, v in self.nii.header.items():
            g.gen(k, str(v), parent=root.nodeid)

        # Save the named graph - the header is tested first so we can stop
        # if there are differences.
        self.graphs["header"] = g

        # TODO we need an added rule that can match based on voxel location
        # and do a subtraction.
        data = self.nii.get_data()
        assert data
        # 1. subtracts the images
        # 2. counts every time the absolute difference is greater than the default tolerance (default 1e-8)
