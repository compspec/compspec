.. _getting-started-asp:

=================
ASP Compatibility
=================

Conceptually, for a:

 - Diff: we will create two graphs and subtract one from the other
 - Composition: we will create one graph and display it

And the neat thing about this approach is that we can take a larger graph and break
it into smaller graphs, and test smaller graphs until we hit a result that suggests an incompatibility,
and stop. Given you are using subgraphs, it means that for some problem space we won't
get a listing of all the incompatible nodes, but we can be fairly sure that the combination
won't work because 1 incompatibility or difference is too much. Of course this design
and how the graphs are presented and tested can be tweaked for any particular problem space.
This part of the project was worked on in 2022 and hasn't been updated since.

.. toctree::
   :maxdepth: 2

   background
   user-guide
   spec.md
