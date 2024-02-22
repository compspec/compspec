% A logic program to compare voxels

matching_voxels(A, B, Coord) :-
  node(A, _, "voxel", Coord),
  node(B, _, "voxel", Coord),
  A!=B.

different_values(A, B, ValueA, ValueB) :-
  matching_voxels(A, B, Coord),
  node(A, _, "value", ValueA),
  node(B, _, "value", ValueB),
  ValueA != ValueB,
  A != B.

too_different(A, B, ValueA, ValueB) :-
  different_values(A, B, ValueA, ValueB), (ValueA - ValueB) > 1.

#show different_values/4.
#show too_different/4.
