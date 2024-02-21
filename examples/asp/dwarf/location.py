__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import re

from elftools.dwarf.descriptions import ExprDumper
from elftools.dwarf.locationlists import LocationEntry

# Keep a cache of dumpers with lookup based on the struct
_DWARF_EXPR_DUMPER_CACHE = {}


def get_dwarf_from_expr(expr, structs, cu_offset=None):
    cache_key = id(structs)
    if cache_key not in _DWARF_EXPR_DUMPER_CACHE:
        _DWARF_EXPR_DUMPER_CACHE[cache_key] = RegisterDumper(structs)
    dwarf_expr_dumper = _DWARF_EXPR_DUMPER_CACHE[cache_key]
    return dwarf_expr_dumper.dump_register(expr, cu_offset)


def get_loclist(loclist, die):
    """
    Get the parsed location list
    """
    registers = []
    for loc_entity in loclist:
        if isinstance(loc_entity, LocationEntry):
            registers.append(
                get_register_from_expr(
                    loc_entity.loc_expr, die.dwarfinfo.structs, die.cu.cu_offset
                )
            )
        else:
            registers.append(str(loc_entity))
    return registers


def parse_register(register):
    """
    Given the first register entry, remove dwarf tag, etc.
    """
    # DW_OP_fbreg is signed LEB128 offset from  the DW_AT_frame_base address of the current function.
    if "DW_OP_fbreg" in register:
        return "framebase" + register.split(":")[-1].strip()

    # If we have a ( ) this is the register name
    if re.search(r"\((.*?)\)", register):
        return "%" + re.sub("(\(|\))", "", re.search(r"\((.*?)\)", register).group(0))
    # Still need to parse
    if register == "null":
        return None
    return register


def get_register_from_expr(expr, structs, cu_offset=None):
    """
    A tweaked https://github.com/eliben/pyelftools/blob/master/elftools/dwarf/descriptions.py#L135
    to allow parsing the expression to just get the register.
    """
    cache_key = id(structs)
    if cache_key not in _DWARF_EXPR_DUMPER_CACHE:
        _DWARF_EXPR_DUMPER_CACHE[cache_key] = RegisterDumper(structs)
    dwarf_expr_dumper = _DWARF_EXPR_DUMPER_CACHE[cache_key]
    return dwarf_expr_dumper.dump_register(expr, cu_offset)


class RegisterDumper(ExprDumper):
    """A dumper to get registers from an expression."""

    def dump_register(self, expr, cu_offset=None):
        """
        Parse a DWARF expression (list of integer values) into the register.
        """
        parsed = self.expr_parser.parse_expr(expr)
        registers = []
        for deo in parsed:
            registers.append(
                self._dump_to_string(deo.op, deo.op_name, deo.args, cu_offset)
            )
        return registers
