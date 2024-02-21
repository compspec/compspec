import importlib
import os
import pkgutil

import jsonschema

import compspec.utils as utils
from compspec.schema import jgf_v2


class PluginRegistry:
    """
    A base plugin registry to support eventual executors, checkers, etc.
    """

    def __init__(self):
        self.discover()

    def get_plugin_names(self):
        return list(self.plugins)

    def is_installed(self, name):
        return name in self.plugins

    def get_plugin(self, name):
        plugin = self.plugins.get(name)
        if plugin is None:
            raise ValueError(f"Plugin {name} is not known.")
        return plugin

    def add_arguments(self, subparser):
        """
        Add subparser and arguments for each plugin
        """
        for _, plugin in self.plugins.items():
            plugin.add_arguments(subparser)

    def discover(self):
        """
        Discover and register plugins with name compspec-<name>
        """
        self.plugins = {}
        for moduleinfo in pkgutil.iter_modules():
            if not moduleinfo.ispkg or not moduleinfo.name.startswith(
                self.module_prefix
            ):
                continue
            module = importlib.import_module(moduleinfo.name)
            self.register(moduleinfo.name, module)

    def register(self, name, plugin):
        """
        Register a new plugin.
        """
        if name in self.plugins:
            return
        self.validate_plugin(name, plugin)

        # Python modules use "_" instead of "-"
        name = name.removeprefix(self.module_prefix).replace("_", "-")
        self.plugins[name] = self.load_plugin(name, plugin)

    def load_plugin(self, name, module):
        """
        Load an extractor plugin
        """
        p = getattr(module, self.plugin_class)
        return p(name)

    def validate_plugin(self, name, module):
        """
        Validate a plugin.
        """
        invalid = f"Plugin {name} is not valid"

        # Plugin must be defined!
        if not hasattr(module, self.plugin_class):
            raise ValueError(f"{invalid}, missing {self.plugin_class} to import")

        cls = getattr(module, self.plugin_class)
        if not hasattr(cls, "description"):
            raise ValueError(f"{invalid}, missing 'description' attribute")
        if not cls.description:
            raise ValueError(f"{invalid},'description' attribute is not defined")

        # First look for schema.json
        schema_dir = os.path.abspath(module.__path__[0])

        # 1. Schema directory must exist
        if not os.path.exists(schema_dir):
            raise ValueError(f"{invalid}, schema directory {schema_dir} does not exist")

        # 2. Schema file must also exist
        schema_file = os.path.join(schema_dir, "schema.json")
        if not os.path.exists(schema_file):
            raise ValueError(f"{invalid} schema file {schema_file} does not exist")

        # 3. Load and validate JGF
        schema = utils.read_json(schema_file)
        jsonschema.validate(schema, schema=jgf_v2)


class ExtractorRegistry(PluginRegistry):
    """
    A Registry for extractor plugins that retrieve metadata.
    """

    plugin_class = "ExtractorPlugin"
    module_prefix = "compspec_"
