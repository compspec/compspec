.. _getting_started-abi-user-guide:

==========
User Guide
==========

Compspec provides a plugin-based strategy to extract metadata about some application or environment.
We currently support the following extractor plugins:

 - `compspec-ior <https://github.com/compspec/compspec-ior>`_: for I/O metadata

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
