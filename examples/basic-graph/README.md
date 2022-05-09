# Basic Graph

A basic graph is a single composition for something. In this example, we define
a graph for a function and some nested attributes, and we show creating
the composition, running to output ASP facts, and then providing our own
logic program to ask to show the unique node and relation types.

```bash
python run.py

...
%============================================================================
% Composition Namespace A
%============================================================================
namespace("A").
node("A","id0","func","goodbye_world").
node("A","id1","func","hello_world").
node("A","id3","parameter","name").
node("A","id4","default","Vanessa").
relation("A","id1","has","id3").
relation("A","id3","has","id4").
relation("A","id3","has","id5").
relation("A","id1","has","id6").
relation("A","id6","has","id7").
{'unique_node_types': [['func'], ['parameter'], ['default']], 'unique_relation_types': [['has']]}
```

Note that this is running in a verbose mode (the default) and if you don't want the
facts to be output you can set quiet to True:

```python
c = Composition(A, namespace="A", quiet=True)
c.run()
```
