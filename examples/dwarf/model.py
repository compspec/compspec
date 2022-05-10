__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

# This is the base model for deriving the DWARF graphs and then
# running the comparison (used in all the examples)

from compspec.runner import Difference
from compspec.runner.base import FactGenerator as FactGeneratorBase
import compspec.solver
from compspec.solver import fn
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)

# Parsing dwarf requires a basic corpus and DwarfParser
from corpus import Corpus
from dwarf import DwarfParser


class DwarfDifference(Difference):
    """
    Calculate a diff between two ELF + Dwarf binaries.
    """

    def __init__(self, lib1, lib2, out=None, quiet=False):
        self.driver = compspec.solver.PyclingoDriver(out=out)
        self.facts = FactGenerator(lib1, lib2)
        self.set_verbosity(out, quiet)


class FactGenerator(FactGeneratorBase):
    """
    The FactGenerator takes two libraries and generates facts for the solver.
    We do this by loading them as a corpus.
    """

    def __init__(self, lib1, lib2):
        self.lib1 = lib1
        self.lib2 = lib2
        self.A = Corpus(lib1)
        self.B = Corpus(lib2)

    def setup(self, driver):
        """
        Setup data for two libraries to prepare for the solve.
        """
        self.gen = driver
        self.gen.h1("Difference Calcultion for Dwarf")

        # The basename for each is the namespace
        self.gen.fact(fn.is_a(self.A.basename))
        self.gen.fact(fn.is_b(self.B.basename))

        self.gen.h2("Library: %s" % self.A.basename)

        # Dwarf information entry parser to yield information
        # This is a subclass of compspec.graph.Graph
        A = DwarfParser(self.A)
        B = DwarfParser(self.B)
        self.generate_facts(A, self.A.basename)
        self.generate_facts(B, self.B.basename)
