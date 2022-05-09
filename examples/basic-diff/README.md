# Basic Diff

If we take two graphs, such as from the [basic-graph](../basic-graph) example,
given that they describe two different states to compare, we can calculate a simple diff.
In this example, we define two graphs for a function and some changed nested attributes, 
and we show calculating the diff, first just using the default comparison provided by
compspec, and then adding a custom program to output more information about
unique node and relation types.

```bash
python run.py
...

%============================================================================
% Difference Betweeen A and B
%============================================================================
is_a("A").
is_b("B").

%----------------------------------------------------------------------------
% Namespace A
%----------------------------------------------------------------------------
node("A","id0","func","goodbye_world").
node("A","id1","func","hello_world").
node("A","id3","parameter","name").
node("A","id4","default","Vanessa").
relation("A","id1","has","id3").
relation("A","id3","has","id4").
relation("A","id3","has","id5").
relation("A","id1","has","id6").
relation("A","id6","has","id7").
node("B","id0","func","goodbye_world").
node("B","id1","func","hello_world").
node("B","id3","parameter","name").
node("B","id4","default","Squidward").
relation("B","id1","has","id3").
relation("B","id3","has","id4").
relation("B","id3","has","id5").
relation("B","id1","has","id6").
relation("B","id6","has","id7").
{'is_a': [['A']], 'is_b': [['B']], 'unique_namespace_node_types': [['A', 'func'], ['A', 'parameter'], ['A', 'default'], ['B', 'func'], ['B', 'parameter'], ['B', 'default']], 'unique_namespace_relation_types': [['A', 'has'], ['B', 'has']], 'unique_node_types': [['func'], ['parameter'], ['default']], 'unique_relation_types': [['has']], 'is_different': [['A', 'B']], 'changed_node_value': [['A', 'B', 'id4', 'id4', 'default', 'Vanessa', 'Squidward']]}
```

And here we see the set of rules we provided (unique_*) and also facts for the diff. E.g.,
that the default parameter of name "Vanessa" changed to "Squidward."


