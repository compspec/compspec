% An example logic program to show unique node types (the names) and relation types

unique_namespace_node_types(Namespace, N) :- node(Namespace, _, N, _).
unique_namespace_relation_types(Namespace, R) :- relation(Namespace, _, R, _).

unique_node_types(N) :- node(_, _, N, _).
unique_relation_types(R) :- relation(_, _, R, _).

#show unique_node_types/1.
#show unique_relation_types/1.
#show unique_namespace_node_types/2.
#show unique_namespace_relation_types/2.
