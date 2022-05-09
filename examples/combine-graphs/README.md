# Combine Graphs

A basic graph is a single composition for something. What if we want to generate
multiple graphs, and combine the facts into a single space? This example shows how to
do that.

```bash
python run.py

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

%============================================================================
% Composition Namespace B
%============================================================================
namespace("B").
node("B","id0","func","goodbye_world").
node("B","id1","func","hello_world").
node("B","id3","parameter","name").
node("B","id4","default","Squidward").
relation("B","id1","has","id3").
relation("B","id3","has","id4").
relation("B","id3","has","id5").
relation("B","id1","has","id6").
relation("B","id6","has","id7").
{'unique_namespace_node_types': [['A', 'func'], ['A', 'parameter'], ['A', 'default'], ['B', 'func'], ['B', 'parameter'], ['B', 'default']], 'unique_namespace_relation_types': [['A', 'has'], ['B', 'has']], 'unique_node_types': [['func'], ['parameter'], ['default']], 'unique_relation_types': [['has']]}
```
