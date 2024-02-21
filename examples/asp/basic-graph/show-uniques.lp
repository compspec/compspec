% An example logic program to show unique node types (the names) and relation types

unique_node_types(N) :- node(_, _, N, _).
unique_relation_types(R) :- relation(_, _, R, _).

#show unique_node_types/1.
#show unique_relation_types/1.
