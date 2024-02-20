.. _getting_started-abi-user-guide:

==========
User Guide
==========

The core client here is intended to be used as an API, meaning you can derive
facts and relations and then run a model. It is intended for higher level libraries
to use this module for custom command line parsing of specific domain-oriented entities.
If you haven't read  :ref:`getting_started-installation` you should do that first.

Examples
========

For full examples, try running the scripts under `examples <https://github.com/compspec/compspec/tree/main/examples/asp>`_ after you install
compspec. We will be adding a sphinx gallery with full examples here.

.. code-block:: console

    $ python examples/asp/basic-graph/run.py
    $ python examples/asp/basic-diff/run.py
    $ python examples/asp/combine-graphs/run.py

The dwarf examples have a Makefile to build with ``make`` and then can be run
based on the name. See the `README.md for dwarf <https://github.com/compspec/compspec/tree/main/examples/asp/dwarf>`_ for how to do this.
We also have an example that takes an iterative approach to compare groups:

.. code-block:: console

    $ python examples/asp/python/tensorflow-module-example.py
    $ python examples/asp/python/tensorflow-function-example.py
    $ python examples/asp/python/tensorflow-example.py

That example is best if you are interested in breaking a problem space into
multiple graphs.


Additional Functionality
========================

Given that you have a graph:

.. code-block:: python

    A = Graph()
    for node_id, name, value in [
        ["id0", "func", "goodbye_world"],
        ["id1", "func", "hello_world"],
        ["id3", "parameter", "name"],
        ["id4", "default", "Squidward"],
    ]:
        A.new_node(name, value, node_id)

    for fromid, relation, toid in [
        ["id1", "has", "id3"],
        ["id3", "has", "id4"],
        ["id3", "has", "id5"],
        ["id1", "has", "id6"],
        ["id6", "has", "id7"],
    ]:
        A.new_relation(fromid, toid, relation)

You can convert it to a dictionary:


.. code-block:: python

    obj = A.to_dict()


And given that loaded (e.g., from json), we can then populate a new graph!


.. code-block:: python

    g = Graph.from_dict(obj)


These are very simple operations to define graphs, and primarily the work is done
manually to create the nodes, relations, and identifiers. It is expected that specific
domains that intend to create graphs will load in some object (e.g., a binary file) and 
do this creation on behalf of the user.
