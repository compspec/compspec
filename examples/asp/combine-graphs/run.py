import os

from compspec.asp import Combination
from compspec.graph import Graph

here = os.path.dirname(os.path.abspath(__file__))


def main():
    # Create graphs A and B
    A = Graph()

    # Create graph for some namespace A
    for node_id, name, value in [
        ["id0", "func", "goodbye_world"],
        ["id1", "func", "hello_world"],
        ["id3", "parameter", "name"],
        ["id4", "default", "Vanessa"],
    ]:
        A.new_node(name, value, node_id)

    # Add relations to A
    for fromid, relation, toid in [
        ["id1", "has", "id3"],
        ["id3", "has", "id4"],
    ]:
        A.new_relation(fromid=fromid, toid=toid, relation=relation)

    # Do the same for a graph B
    B = Graph()
    for node_id, name, value in [
        ["id0", "func", "goodbye_world"],
        ["id1", "func", "hello_world"],
        ["id3", "parameter", "name"],
        ["id4", "default", "Squidward"],
    ]:
        B.new_node(name, value, node_id)

    for fromid, relation, toid in [
        ["id1", "has", "id3"],
        ["id3", "has", "id4"],
    ]:
        B.new_relation(fromid=fromid, toid=toid, relation=relation)

    # Now let's combine into one graph
    c = Combination()
    c.add_graph(A, "A")
    c.add_graph(B, "B")
    c.run()

    # We can also provide an example logic program!
    lp = os.path.join(here, "show-uniques.lp")
    res = c.run(lp)
    print(res)


if __name__ == "__main__":
    main()
