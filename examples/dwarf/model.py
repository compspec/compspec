__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import compspec.graph
from elftools.common.py3compat import bytes2str
from elftools.dwarf.descriptions import (
    describe_attr_value,
    set_global_machine_arch,
)
from elftools.dwarf.locationlists import LocationParser, LocationExpr
from elftools.dwarf.dwarf_expr import DWARFExprParser

import os
import sys
import re
import uuid
import subprocess

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)
import location
from corpus import Corpus

# Human friendly names for general tag "types"
known_die_types = {"DW_TAG_array_type": "array"}

# These namespace regular expressions indicate connectors, meaning they are
# part of the graph but not included in the set of interest (just an is_connector)
skip_namespaces = ["std", "^__", "^11__", "FILE", "gnu_cxx", "GLOBAL"]
skip_regex = "(%s)" % "|".join(skip_namespaces)


def demangle(names):
    """
    Supporting function to run c++filt to demangle.
    """
    args = ["c++filt", *names]
    pipe = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = pipe.communicate()
    return [x for x in stdout.decode("utf-8").split("\n") if x]


class DwarfGraph(compspec.graph.Graph):
    """
    A subclass of Graph to add nodes / relations that are for dwarf.

    Note implementation wise, a subclass of graph can either:
    1. add a custom iter_nodes, iter_relations function to provide those, OR
    2. parse into self.nodes (dict) or self.relations (list) separately.

    For the DWARF example here we do #2 because the examples are small/simple,
    however a different implementation could yield them instead. A better
    implementation would figure out how to do the comparison in pieces so
    we can cut out early.
    """

    def __init__(self, lib, scope=None):
        self.corpus = Corpus(lib)
        super().__init__()
        self.type_lookup = self.corpus.get_type_lookup()
        self.children_lookup = {}
        self._prepare_location_parser()

        # line programs we will include in scope
        scope = scope or []
        self._set_accepted_line_programs(scope)

        # Hard coded for examples
        self.extract()

    def _set_accepted_line_programs(self, names):
        """
        We can filter out a lot of a noisy external namespace by scoping to line programs
        """
        self._accepted_line_programs = set()
        if not isinstance(names, list):
            names = names
        for name in names:
            for lp in self.corpus.line_programs:
                if name in lp:
                    self._accepted_line_programs.add(self.corpus.line_programs[lp])

    def _prepare_location_parser(self):
        """
        Prepare the location parser using the dwarf info
        """
        location_lists = self.corpus.location_lists

        # Needed to decode register names in DWARF expressions.
        set_global_machine_arch(self.corpus.machine_arch)
        self.loc_parser = LocationParser(location_lists)

    def extract(self):
        """
        Note that if we wanted to yield facts, the class here could
        re-implement iter_nodes and iter_relations instead of calling this
        to be done first!
        """
        for die in self.corpus.iter_dwarf_information_entries():
            if not die or not die.tag:
                continue
            # Generate facts for the DIE
            self.facts(die)

    def generate_parent(self, die, parent=None):
        """
        Generate the parent, if one exists.
        relation("A", "id6", "has", "id7").
        """
        if not parent:
            parent = die.get_parent()
        if parent:
            self.add_to_lookup(parent)
            self.new_relation(self.ids[parent], "has", self.ids[die])

    def add_to_lookup(self, die):
        if die not in self.ids:
            self.ids[die] = self.next()
        self.lookup[die.offset] = self.ids[die]

    def in_lookup(self, die):
        return die.offset in self.lookup

    def remove_from_lookup(self, die):
        if die in self.ids:
            del self.ids[die]
        if die.offset in self.lookup:
            del self.lookup[die.offset]

    def facts(self, die):
        """
        Yield facts for a die. We keep track of ids and relationships here.
        """
        # Have we parsed it yet?
        if die.offset in self.lookup:
            return

        # Assume we are parsing all dies
        self.add_to_lookup(die)

        if die.tag == "DW_TAG_namespace":
            return self.parse_namespace(die)

        if die.tag == "DW_TAG_compile_unit":
            return self.parse_compile_unit(die)

        if die.tag == "DW_TAG_class_type":
            return self.parse_class_type(die)

        if die.tag == "DW_TAG_subprogram":
            return self.parse_subprogram(die)

        if die.tag == "DW_TAG_formal_parameter":
            return self.parse_formal_parameter(die)

        if die.tag == "DW_TAG_inheritance":
            # This is handled under classes and structs
            return

        # If we are consistent with base type naming, we don't
        # need to associate a base type size with everything that uses it,
        # but rather just the one base type
        if die.tag == "DW_TAG_base_type":
            return self.parse_base_type(die)

        if die.tag == "DW_TAG_variable":
            return self.parse_variable(die)

        if die.tag == "DW_TAG_pointer_type":
            return self.parse_pointer_type(die)

        if die.tag == "DW_TAG_structure_type":
            return self.parse_structure_type(die)

        if die.tag == "DW_TAG_member":
            return self.parse_member(die)

        if die.tag == "DW_TAG_array_type":
            return self.parse_array_type(die)

        if die.tag == "DW_TAG_subrange_type":
            return self.parse_subrange_type(die)

        if die.tag == "DW_TAG_typedef":
            return self.parse_typedef(die)

        if die.tag == "DW_TAG_const_type":
            return self.parse_const_type(die)

        if die.tag in ["DW_TAG_imported_module", "DW_TAG_imported_declaration"]:
            return self.parse_imported_module(die)

        if die.tag == "DW_TAG_template_type_param":
            return self.parse_template_type_param(die)

        if die.tag == "DW_TAG_template_value_param":
            return self.parse_template_value_param(die)

        if die.tag == "DW_TAG_enumeration_type":
            return self.parse_enumeration_type(die)

        if die.tag == "DW_TAG_enumerator":
            return self.parse_enumerator(die)

        if die.tag == "DW_TAG_union_type":
            return self.parse_union_type(die)

        if die.tag == "DW_TAG_unspecified_parameters":
            return self.parse_unspecified_parameters(die)

        if die.tag == "DW_TAG_unspecified_type":
            return self.parse_unspecified_type(die)

        if die.tag == "DW_TAG_reference_type":
            return self.parse_reference_type(die)

        if die.tag == "DW_TAG_subroutine_type":
            return self.parse_subroutine_type(die)

        if die.tag == "DW_TAG_rvalue_reference_type":
            return self.parse_rvalue_reference_type(die)

        # TODO haven't seen these yet
        print(die)
        import IPython

        IPython.embed()
        sys.exit()

        if die.tag == "DW_TAG_lexical_block":
            return self.parse_die(die)

        # Legical blocks wrap other things
        if die.tag == "DW_TAG_lexical_block":
            return self.parse_children(die)

    def parse_sized_generic(self, die, name, node_name=None, is_connector=False):
        """
        parse a sized generic, meaning a named type with a parent and size.
        """
        is_connector = is_connector or self.is_connector(die)
        node_name = node_name or get_name(die)
        self.new_node(name, node_name, self.ids[die], is_connector=is_connector)
        self.generate_parent(die)
        size = get_size(die)
        if size != "unknown":
            self.gen("size", size, parent=self.ids[die], is_connector=is_connector)

    def parse_base_type(self, die):
        self.parse_sized_generic(die, "basetype")

    def parse_class_type(self, die):
        self.parse_sized_generic(die, "class")
        self.check_inheritance(die)

    def parse_namespace(self, die):
        """
        Parse a namespace, which is mostly a name and relationship
        """
        self.new_node(
            "namespace",
            get_name(die),
            self.ids[die],
            is_connector=self.is_connector(die),
        )
        self.generate_parent(die)

    def parse_imported_module(self, die):
        """
        Parse an imported module (this likely isn't an ABI break by why not
        """
        imported = self.type_lookup[die.attributes["DW_AT_import"].value]
        self.new_node(
            "imports",
            get_name(imported),
            self.ids[die],
            is_connector=self.is_connector(die),
        )
        self.generate_parent(die)

    def parse_const_type(self, die):
        """
        Parse a constant type
        """
        underlying_type = self.get_underlying_type(die)

        # Not sure what this is - a pretty much empty DIE
        if underlying_type == "unknown" and not die.has_children:
            return
        self.new_node(
            "const", underlying_type, self.ids[die], is_connector=self.is_connector(die)
        )
        self.generate_parent(die)

    def parse_typedef(self, die):
        """
        Parse a type definition
        """
        is_connector = self.is_connector(die)
        self.new_node(
            "typedef", get_name(die), self.ids[die], is_connector=is_connector
        )
        self.generate_parent(die)
        self.gen(
            "type",
            self.get_underlying_type(die),
            parent=self.ids[die],
            is_connector=is_connector,
        )

    def parse_reference_type(self, die):
        """
        Parse a reference type. Also don't include these directly (connectors)
        """
        self.parse_sized_generic(die, "reference", is_connector=True)
        self.gen(
            "type",
            self.get_underlying_type(die),
            parent=self.ids[die],
            is_connector=True,
        )

    def parse_subroutine_type(self, die):
        """
        Parse a subroutine type
        """
        name = get_name(die)
        if name == "unknown":
            name = self.get_underlying_type(die)
        if name == "unknown":
            return
        is_connector = self.is_connector(die)
        self.new_node("subroutine", name, self.ids[die], is_connector=is_connector)
        self.generate_parent(die)
        self.gen(
            "type",
            self.get_underlying_type(die),
            parent=self.ids[die],
            is_connector=is_connector,
        )

    def parse_rvalue_reference_type(self, die):
        """
        Parse an rvalue reference type
        """
        self.parse_sized_generic(die, "rvalue_reference", is_connector=True)
        self.gen(
            "type",
            self.get_underlying_type(die),
            parent=self.ids[die],
            is_connector=True,
        )

    def parse_unspecified_parameters(self, die):
        """
        This die appears to be empty, so just parse the relationship
        """
        self.new_node(
            "unspecified_parameters", get_name(die), self.ids[die], is_connector=True
        )
        self.generate_parent(die)

    def parse_unspecified_type(self, die):
        self.new_node(
            "unspecified_type",
            get_name(die),
            self.ids[die],
            is_connector=self.is_connector(die),
        )
        self.generate_parent(die)

    def parse_template_type_param(self, die):
        """
        Parse a template type param
        """
        is_connector = self.is_connector(die)
        self.new_node(
            "template_type_param",
            get_name(die),
            self.ids[die],
            is_connector=is_connector,
        )
        self.generate_parent(die)
        self.gen(
            "type",
            self.get_underlying_type(die),
            parent=self.ids[die],
            is_connector=is_connector,
        )

    def parse_template_value_param(self, die):
        """
        Parse a template value param
        """
        self.parse_template_type_param(die)
        self.gen(
            "constvalue",
            die.attributes["DW_AT_const_value"].value,
            parent=self.ids[die],
            is_connector=self.is_connector(die),
        )

    def is_external(self, die):
        value = die.attributes.get("DW_AT_external")
        if value:
            return value.value
        return False

    def parse_formal_parameter(self, die):
        """
        Parse a formal parameter
        """
        parent = die.get_parent()
        actual_parent = None

        # If the parent references another, use that one
        if "DW_AT_specification" in parent.attributes:
            actual_parent = self.type_lookup[
                parent.attributes["DW_AT_specification"].value
            ]

        # Don't parse for now if no name, or parent is external
        name = get_name(die)
        if name == "unknown":
            self.remove_from_lookup(die)
            return

        is_connector = self.is_connector(die)
        self.new_node(
            "parameter", get_name(die), self.ids[die], is_connector=is_connector
        )
        if actual_parent:
            if actual_parent.offset in self.lookup:
                parent_id = self.lookup[actual_parent.offset]
                parent_node = self.nodes[parent_id]
                self.new_relation(parent_id, "has", self.ids[die])
        else:
            self.generate_parent(die)

        size = get_size(die)
        if size != "unknown":
            self.gen(
                "size", get_size(die), parent=self.ids[die], is_connector=is_connector
            )
        self.gen(
            "type",
            self.get_underlying_type(die),
            parent=self.ids[die],
            is_connector=is_connector,
        )
        loc = self.parse_location(die)
        if not loc:
            return
        self.gen("location", loc, parent=self.ids[die], is_connector=is_connector)

        parent = actual_parent or parent
        order = 0
        for child in parent.iter_children():
            if child == die:
                self.gen(
                    "order", order, parent=self.ids[die], is_connector=is_connector
                )
                break
            else:
                order += 1
        return

    def parse_pointer_type(self, die):
        """
        Parse a pointer.

        We don't want to parse this directly, usually it will be an underlying
        type of something.
        """
        self.parse_sized_generic(die, "pointer", is_connector=True)

    def parse_member(self, die):
        """
        Parse a member, typically belonging to a union
        Note these can have DW_AT_data_member_location but we arn't parsing
        """
        # This returns a string representation!
        underlying_type = self.get_underlying_type(die)

        # If it's an array, we need to get the member type
        member_type = None
        if underlying_type == "array":
            array = self.get_underlying_type(die, return_die=True)
            member_type = self.get_underlying_type(array)

        is_connector = self.is_connector(die)
        self.new_node("member", get_name(die), self.ids[die], is_connector=is_connector)
        self.gen(
            "type", underlying_type, parent=self.ids[die], is_connector=is_connector
        )
        if member_type:
            self.gen(
                "membertype",
                member_type,
                parent=self.ids[die],
                is_connector=is_connector,
            )
        self.generate_parent(die)

        # This should be a struct or similar
        parent = die.get_parent()
        if parent:

            # Get the order of the member - it matters if it changes
            if parent not in self.ids:
                self.ids[parent] = self.next()
            for i, child in enumerate(parent.iter_children()):
                if child == die:
                    node, _ = self.gen(
                        "order", i, parent=self.ids[die], is_connector=is_connector
                    )
                    self.new_relation(self.ids[die], "has", node.nodeid)

    def is_connector(self, die):
        """
        Check 1. the die variable name starting with __ (compiler internal) and
        Check 2. any parent up to a root in the skip namespaces
        """
        # It doesn't have any attributes
        if not die.attributes:
            return True

        # If the line program isn't in our interested set (hard coded always to example.cpp for now)
        if "DW_AT_decl_file" in die.attributes:
            line_program = die.attributes["DW_AT_decl_file"].value
            if line_program not in self._accepted_line_programs:
                return True

        # Underlying type outside in skip lists
        if re.search(skip_regex, self.get_underlying_type(die)):
            return True

        if "DW_AT_specification" in die.attributes:
            spec = self.type_lookup[die.attributes["DW_AT_specification"].value]
            if re.search(skip_regex, get_name(spec)):
                return True

        if self.is_compiler_internal(die) or re.search(skip_regex, get_name(die)):
            return True

        # Check demangled names
        names = []
        if "DW_AT_linkage_name" in die.attributes:
            names.append(bytes2str(die.attributes["DW_AT_linkage_name"].value))

        parent = die.get_parent()
        while parent:
            if re.search(skip_regex, get_name(parent)):
                return True
            if "DW_AT_linkage_name" in parent.attributes:
                names.append(bytes2str(parent.attributes["DW_AT_linkage_name"].value))
            parent = parent.get_parent()

        # Check each DW_AT_sibling for DW_AT_specification
        while "DW_AT_sibling" in die.attributes:
            die = self.type_lookup[die.attributes["DW_AT_sibling"].value]
            if re.search(skip_regex, get_name(die)):
                return True
            if "DW_AT_specification" in die.attributes:
                spec = self.type_lookup[die.attributes["DW_AT_specification"].value]
                if re.search(skip_regex, get_name(spec)):
                    return True

        # Demangle names
        if names:
            for name in demangle(names):
                if re.search(skip_regex, name):
                    return True
        return False

    def parse_structure_type(self, die, is_connector=False):
        """
        Parse a structure type.
        """
        size = get_size(die)
        if size != "unknown":
            self.parse_sized_generic(die, "structure")
        else:
            self.new_node(
                "structure",
                get_name(die),
                self.ids[die],
                is_connector=self.is_connector(die),
            )
            self.generate_parent(die)
        self.check_inheritance(die)

    def check_inheritance(self, die):
        """
        If a die has inheritance, make sure we capture and show order.
        """
        # Look for inherited classes
        inherit_order = 0
        for child in die.iter_children():
            if child.tag == "DW_TAG_inheritance":

                # This is the actual inherited die
                inherited = self.type_lookup[child.attributes["DW_AT_type"].value]
                self.gen(
                    "inherits",
                    get_name(inherited) + ":" + str(inherit_order),
                    parent=self.ids[die],
                    is_connector=self.is_connector(die),
                )
                inherit_order += 1

    def is_compiler_internal(self, die):
        """
        Determine if a symbol belongs to the compiler internal namespace
        """
        return get_name(die).startswith("__")

    def parse_variable(self, die):
        """
        Parse a variable
        """
        name = get_name(die)
        underlying_type = self.get_underlying_type(die)

        if name == "unknown" and "DW_AT_specification" in die.attributes:
            spec = self.type_lookup[die.attributes["DW_AT_specification"].value]
            is_connector = self.is_connector(die) or self.is_connector(spec)
            name = get_name(spec)
            self.get_underlying_type(spec)
        else:
            is_connector = self.is_connector(die)

        self.parse_sized_generic(die, "variable", node_name=name)
        self.gen(
            "type", underlying_type, parent=self.ids[die], is_connector=is_connector
        )
        loc = self.parse_location(die)
        if not loc:
            return
        self.gen("location", loc, parent=self.ids[die], is_connector=is_connector)

    def parse_subprogram(self, die):
        """
        Add a function (subprogram) parsed from DWARF
        """
        name = get_name(die)
        if name == "unknown":
            self.remove_from_lookup(die)
            return

        self.new_node(
            "function",
            get_name(die),
            self.ids[die],
            is_connector=self.is_connector(die),
        )
        self.generate_parent(die)

    def parse_array_type(self, die):
        """
        Get an entry for an array.
        """
        # Don't parse if we don't have a name, it's likely referenced from a member
        name = get_name(die)
        if name == "unknown":
            self.remove_from_lookup(die)
            return

        is_connector = self.is_connector(die)
        self.new_node("array", get_name(die), self.ids[die], is_connector=is_connector)
        self.generate_parent(die)
        self.gen(
            "membertype",
            self.get_underlying_type(die),
            parent=self.ids[die],
            is_connector=is_connector,
        )

        if "DW_AT_ordering" in die.attributes:
            self.gen(
                "order",
                die.attributes["DW_AT_ordering"].value,
                parent=self.ids[die],
                is_connector=is_connector,
            )

        # Case 1: the each member of the array uses a non-traditional storage
        member_size = self._find_nontraditional_size(die)
        if member_size:
            self.gen(
                "membersize",
                member_size,
                parent=self.ids[die],
                is_connector=is_connector,
            )

    def parse_enumeration_type(self, die):
        """
        Parse an enumeration type!
        """
        self.parse_sized_generic(die, "enum")
        self.gen(
            "type",
            self.get_underlying_type(die),
            parent=self.ids[die],
            is_connector=self.is_connector(die),
        )

    def parse_enumerator(self, die):
        """
        Parse enumerator.
        """
        is_connector = self.is_connector(die)
        self.new_node(
            "enumerator", get_name(die), self.ids[die], is_connector=is_connector
        )
        self.generate_parent(die)
        self.gen(
            "enumerator_const_value",
            die.attributes["DW_AT_const_value"].value,
            parent=self.ids[die],
            is_connector=is_connector,
        )

    def parse_union_type(self, die):
        """
        Parse a union type.
        """
        self.parse_sized_generic(die, "union")

        # TODO An incomplete union won't have byte size attribute and will have DW_AT_declaration attribute.
        # page https://dwarfstd.org/doc/DWARF4.pdf 85
        if "DW_AT_declaration" in die.attributes:
            print("DW_AT_declaration")
            import IPython

            IPython.embed()

    def parse_compile_unit(self, die):
        """
        Parse a top level compile unit.
        """
        # Generate node, parent (unlikely to have one)
        is_connector = self.is_connector(die)
        self.new_node(
            "compileunit", get_name(die), self.ids[die], is_connector=is_connector
        )
        self.generate_parent(die)

        # we could load low/high PC here if needed
        lang = die.attributes.get("DW_AT_language", None)
        if lang:
            die_lang = describe_attr_value(lang, die, die.offset)
            node = self.new_node("language", die_lang, is_connector=is_connector)
            self.new_relation(self.ids[die], "has", node.nodeid)

    def _find_nontraditional_size(self, die):
        """
        Tag DIEs can have attributes to indicate their members use a nontraditional
        amount of storage, in which case we find this. Otherwise, look at member size.
        """
        if "DW_AT_byte_stride" in die.attributes:
            return die.attributes["DW_AT_byte_stride"].value
        if "DW_AT_bit_stride" in die.attributes:
            return die.attributes["DW_AT_bit_stride"].value * 8

    def get_underlying_type(self, die, pointer=False, return_die=False):
        """
        Given a type, parse down to the underlying type (and count pointer indirections)
        """
        if die.tag == "DW_TAG_base_type":
            if return_die:
                return die
            if pointer:
                return "*%s" % get_name(die)
            return get_name(die)

        elif die.tag in ["DW_TAG_structure_type", "DW_TAG_class_type"]:
            if return_die:
                return die
            return get_name(die)

        if "DW_AT_type" not in die.attributes:
            if return_die:
                return die
            return "unknown"

        # Can we get the underlying type?
        type_die = self.type_lookup.get(die.attributes["DW_AT_type"].value)
        if not type_die:
            if return_die:
                return type_die
            return "unknown"

        # Case 1: It's an array (and type is for elements)
        if type_die and type_die.tag in known_die_types:
            if return_die:
                return type_die
            if pointer:
                return "*%s" % known_die_types[type_die.tag]
            return known_die_types[type_die.tag]

        if type_die.tag == "DW_TAG_base_type":
            if return_die:
                return type_die
            if pointer:
                return "*%s" % get_name(type_die)
            return get_name(type_die)

        # Otherwise, keep digging
        elif type_die:
            while "DW_AT_type" in type_die.attributes:

                if type_die.tag == "DW_TAG_pointer_type":
                    pointer = True

                # Stop when we don't have next dies to parse
                next_die = self.type_lookup.get(type_die.attributes["DW_AT_type"].value)
                if not next_die:
                    break
                type_die = next_die

        if type_die:
            return self.get_underlying_type(type_die, pointer)

        if return_die:
            return type_die
        return "unknown"

    def parse_subrange_type(self, die):
        """
        Parse a subrange type
        """
        # If the parent wasn't added, don't parse
        if not self.in_lookup(die.get_parent()):
            self.remove_from_lookup(die)
            return

        print("SUBRANGE TYPE")
        import IPython

        IPython.embed()
        sys.exit()
        is_connector = self.is_connector(die)
        self.new_node(
            "subrange", get_name(die), self.ids[die], is_connector=is_connector
        )
        self.generate_parent(die)
        self.gen(
            "membertype",
            self.get_underlying_type(die),
            parent=self.ids[die],
            is_connector=is_connector,
        )

        # If the upper bound and count are missing, then the upper bound value is unknown.
        count = "unknown"

        # If we have DW_AT_count, this is the length of the subrange
        if "DW_AT_count" in die.attributes:
            count = die.attributes["DW_AT_count"].value

        # If we have both upper and lower bound
        elif (
            "DW_AT_upper_bound" in die.attributes
            and "DW_AT_lower_bound" in die.attributes
        ):
            count = (
                die.attributes["DW_AT_upper_bound"].value
                - die.attributes["DW_AT_lower_bound"].value
            ) + 1

        # If the lower bound value is missing, the value is assumed to be a language-dependent default constant.
        elif "DW_AT_upper_bound" in die.attributes:

            # TODO need to get language in here to derive
            # TODO: size seems one off.
            # The default lower bound is 0 for C, C++, D, Java, Objective C, Objective C++, Python, and UPC.
            # The default lower bound is 1 for Ada, COBOL, Fortran, Modula-2, Pascal and PL/I.
            lower_bound = 0
            count = die.attributes["DW_AT_upper_bound"].value - lower_bound

            # This is a RANGE including the lower value, so +1
            count += 1

        self.gen("count", count, parent=self.ids[die], is_connector=is_connector)

    def parse_location(self, die):
        """
        Look to see if the DIE has DW_AT_location, and if so, parse to get
        registers. The loc_parser is called by elf.py (once) and addde
        to the corpus here when it is parsing DIEs.
        """
        if "DW_AT_location" not in die.attributes:
            return
        attr = die.attributes["DW_AT_location"]
        if self.loc_parser.attribute_has_location(attr, die.cu["version"]):
            loc = self.loc_parser.parse_from_attribute(attr, die.cu["version"])

            # Attribute itself contains location information
            if isinstance(loc, LocationExpr):
                loc = location.get_register_from_expr(
                    loc.loc_expr, die.dwarfinfo.structs, die.cu.cu_offset
                )
                # The first entry is the register
                return location.parse_register(loc[0])

            # List is reference to .debug_loc section
            elif isinstance(loc, list):
                loc = location.get_loclist(loc, die)
                return location.parse_register(loc[0][0])

    ############################ UNDER

    def parse_call_site(self, die, parent):
        """
        Parse a call site
        """
        entry = {}

        # The abstract origin points to the function
        if "DW_AT_abstract_origin" in die.attributes:
            origin = self.type_die_lookup.get(
                die.attributes["DW_AT_abstract_origin"].value
            )
            entry.update({"name": self.get_name(origin)})

        params = []
        for child in die.iter_children():
            # TODO need better param parsing
            if child.tag == "DW_TAG_GNU_call_site_parameter":
                param = self.parse_call_site_parameter(child)
                if param:
                    params.append(param)
            else:
                raise Exception("Unknown call site parameter!:\n%s" % child)

        if entry and params:
            entry["params"] = params
            self.callsites.append(entry)

    def parse_call_site_parameter(self, die):
        """
        Given a callsite parameter, parse the dwarf expression
        """
        param = {}
        loc = self.parse_location(die)
        if loc:
            param["location"] = loc
        if "DW_AT_GNU_call_site_value" in die.attributes:
            expr_parser = DWARFExprParser(die.dwarfinfo.structs)
            expr = die.attributes["DW_AT_GNU_call_site_value"].value
            # print(get_dwarf_from_expr(expr, die.dwarfinfo.structs, cu_offset=die.cu.cu_offset))
        return param

    # TAGs to parse
    def parse_lexical_block(self, die, code=None):
        """
        Lexical blocks typically have variable children?
        """
        for child in die.iter_children():
            if child.tag == "DW_TAG_variable":
                self.parse_variable(child)

            # We found a loop
            elif child.tag == "DW_AT_lexical_block":
                if code == die.abbrev_code:
                    return
                return self.parse_lexical_block(die)

    def parse_sibling(self, die):
        """
        Try parsing a sibling.
        """
        sibling = self.type_die_lookup.get(die.attributes["DW_AT_sibling"].value)
        return self.parse_underlying_type(sibling)

    def add_class(self, die):
        """
        Given a type, add the class
        """
        if die.tag == "DW_TAG_base_type":
            return "Scalar"
        if die.tag == "DW_TAG_structure_type":
            return "Struct"
        if die.tag == "DW_TAG_array_type":
            return "Array"
        return "Unknown"


# Helper functions to parse a die
def get_name(die):
    """
    A common function to get the name for a die
    """
    name = "unknown"
    if "DW_AT_linkage_name" in die.attributes:
        name = bytes2str(die.attributes["DW_AT_linkage_name"].value)
    elif "DW_AT_name" in die.attributes:
        name = bytes2str(die.attributes["DW_AT_name"].value)

    # If we have something like typedef __va_list_tag __va_list_tag
    if "typedef" in name:
        name = name.replace("typedef", "").strip().split(" ")[0]

    # Some names appear to have leading empty spaces?
    return name.strip()


def get_size(die):
    """
    Return size in bytes (not bits)
    """
    size = "unknown"
    if "DW_AT_byte_size" in die.attributes:
        return die.attributes["DW_AT_byte_size"].value
    # A byte is 8 bits
    if "DW_AT_bit_size" in die.attributes:
        return die.attributes["DW_AT_bit_size"].value * 8
    if "DW_AT_data_bit_offset" in die.attributes:
        raise Exception("Found data_bit_offset in die to parse:\n%s" % die)
    return size
