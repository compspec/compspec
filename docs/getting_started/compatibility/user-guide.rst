.. _getting_started-abi-user-guide:

==========
User Guide
==========

Compspec provides a plugin-based strategy to extract metadata about some application or environment.
We currently support the following extractor plugins:

 - `compspec-ior <https://github.com/compspec/compspec-ior>`_: for I/O metadata
 - `compspec-flux <https://github.com/compspec/compspec-flux>`_: for Flux resource graphs

If you haven't read  :ref:`getting_started-installation` you should do that first.
We will give an example in the context of using IOR.

Example with IOR
================

After installing both:

.. code-block:: console

    $ pip install compspec
    $ pip install compspec-ior

You likely want to do an extractor. The general command looks like this:

.. code-block:: console

    $ compspec extract <name> <options>

For example, with IOR (using defaults):

.. code-block:: console

    $ compspec extract ior

And you can add additional arguments for IOR at the end of the line instead of using the defaults.
An extractor can also have custom arguments. If you want to load from file, for example.

.. code-block:: console

    $ compspec extract ior --ior-load ior-data.json

Or if you want to save the compatibility json to file:

.. code-block:: console

    $ compspec extract --outfile test.json ior

We will have more documentation as the library is developed. For example, we will eventually
be able to package and push to registries with ORAS.


Writing a Plugin
================

Naming
------

Here are some early tips to writing plugins.

 - Your plugin name should be ``compspec-<name>`` (for the repository / pypi package) and the module name ``compspec_<name>``
 - If you'd like to be under the compspec org please open an issue on any repository, we'd love to have you!

Organization
------------

A plugin typically has the following structure:

.. code-block:: console

    ├── CHANGELOG.md
    ├── compspec_ior
    │   ├── defaults.py
    │   ├── __init__.py
    │   ├── plugin.py
    │   ├── schema.json
    │   └── version.py
    ├── LICENSE
    ├── MANIFEST.in
    ├── pyproject.toml
    ├── pytest.ini
    ├── README.md
    ├── setup.cfg
    └── setup.py

Of course the testing setup is up to you, but we recommend pytest and linting, etc.

Your Module
-----------

- In the ``__init__.py`` you are required to have a ``Plugin`` that can be imported, which should be your subclass of ``PluginBase`` (described below)
- In the "defaults.py" you must define:
  - a **namespace** for your plugin (e.g., io.compspec.ior, it is typically like a URL but backwards)
  - a **version** for your schema
  - a **schema_url** (raw GitHub URL) where you can programmatically access the schema

All of the above, and your plugin structure, are validated.

Plugin Design
-------------

The plugin should use the ``compspec.plugins.PluginBase`` class. It should define the following class attributes:


.. code-block:: python

    class Plugin(PluginBase):
        """
        The IOR extractor plugin
        """

        # These metadata fields are required (and checked for)
        description = "IOR parallel I/O benchmarks"
        namespace = defaults.namespace
        version = defaults.spec_version
        schema = defaults.schema_url

Those are all validated when your plugin is loaded into the registry, and it will fail with an error if you forget one.
You should next provide a custom parser that has any special arguments / options you want to appear on the compspec command line.
Make sure to namespace them according to your plugin. That might look like this (note it accepts the subparser as an argument):

.. code-block:: python

    def add_arguments(self, subparser):
        """
        Add arguments for the plugin to show up in argparse
        """
        ior = subparser.add_parser(
            self.name,
            formatter_class=argparse.RawTextHelpFormatter,
            description=self.description,
        )
        # Ensure these are namespaced to your plugin
        ior.add_argument(
            "ior_args",
            help="Arguments for IOR (defaults to reasonable set if not defined)",
            nargs="*",
        )
        ior.add_argument(
            "--ior-load",
            dest="ior_load",
            help="Load metadata from this file instead of extraction from system directly.",
        )

You don't need to return anything - by adding to the subparser, it will stick.
You should also provide an "extract" function that takes "args" and "extra" expected from compspec. Your arguments will be available too.

 - This function should return key/value pairs of your metadata.
 - You do not need to namespace them, that will be done for you.


.. code-block:: python

    def extract(self, args, extra):
        """
        Run IOR and map metadata into compspec schema.
        """
        meta = {"field.a": "a", "field.b": "b"}
        return meta

It's entirely up to you how you want to implement this! For IOR, by default we assume running IOR (with user specific command line options).
But we also provide an ``--ior-load`` parameter that the user can specify to just load pre-generated data from file. As a design strategy, we
expose the function to parse this metadata into a flat list of attributes as a courtesy function, in case it is useful outside of using compspec.
Finally, you might want to provide an "in Python" example for using your plugin.

Testing
-------

We provide `GitHub actions <https://github.com/compspec/actions>`_ that you can use to validate your plugin schema. For example:

.. code-block:: yaml

    on:
      pull_request: []

    jobs:
      validate-schema:
        name: Validate schema
        runs-on: ubuntu-latest
        steps:
          - name: Checkout Repository
            uses: actions/checkout@v4
          - name: Validate Schema
            uses: compspec/actions/validate-schema@main
            with:
              schema: ./compspec_myname/schema.json

You should also provide tests that validate installing and using your plugin with compspec.
As an example, this installs both, runs compspec with a few different configurations, and then runs
an "in Python" example that doesn't rely on the compspec command line utility:


.. code-block:: yaml

    jobs:
      test:
        name: Test IOR
        runs-on: ubuntu-latest
        steps:
          - name: Checkout Repository
            uses: actions/checkout@v4
          - name: Install compspec
            run: pip install compspec

          - name: Install compspec-ior
            run: pip install .

          - name: Test with loading data
            run: compspec extract ior --ior-load ./examples/test/ior-data.json

          - name: Test Python
            run: python ./examples/singleton-run.py


For all of the above, you can see `compspec-ior <https://github.com/compspec/compspec-ior>`_ as an example.
