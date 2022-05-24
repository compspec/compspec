# Compspec Python

<p align="center">
  <img height="300" src="https://raw.githubusercontent.com/compspec/spec/main/img/compspec-circle.png">
</p>

A compspec (Composition spec) is a specification and model for comparing things. This means
that we take an abstract and simple approach to model complex systems as graphs (nodes
and relaionshps) and then can compare between graphs or extract corpora (groups of facts) to use later. 
Compspec python, the implementation here, is intended to provide a basic Python 
for using compspec for your own needs.

 - [The Spec](https://github.com/compspec/spec): read about the background, concepts, and design of the specification.

Conceptually, for a:

 - Diff: we will create two graphs and subtract one from the other
 - Composition: we will create one graph and display it
 
And the neat thing about this approach is that we can take a larger graph and break
it into smaller graphs, and test smaller graphs until we hit a result that suggests an incompatibility,
and stop. Given you are using subgraphs, it means that for some problem space we won't
get a listing of all the incompatible nodes, but we can be fairly sure that the combination
won't work because 1 incompatibility or difference is too much. Of course this design
and how the graphs are presented and tested can be tweaked for any particular problem space.
  
See the ⭐️ [Documentation](https://compspec.github.io/compspec) ⭐️ for basic usage
and getting started.

## TODO

- create compspec.yaml where we can explicitly define kinds of ABI breaks?
- look into Go library?
- we need to be able to print out the result (based on graph relationships)
