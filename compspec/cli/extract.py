#!/usr/bin/env python

__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022-2024, Vanessa Sochat"
__license__ = "MIT"

import compspec.artifact
import compspec.utils as utils


def main(args, extra):
    """
    Run an extraction. This can be converted to a proper function
    if needed.
    """
    from compspec.plugin.parser import extractor_registry

    # This raises an error if not found
    plugin = extractor_registry.get_plugin(args.extract)

    # Prepare a compatibility spec, these are attributes (not namespaces)
    attributes = plugin.extract(args, extra)

    # Generate the artifact
    artifact = compspec.artifact.generate(plugin, args.name, attributes)

    if args.outfile:
        utils.write_json(artifact.to_dict(), args.outfile)
    else:
        print(artifact.render())
