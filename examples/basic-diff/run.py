from compspec.graph import Graph
from compspec.runner import Difference
import os

here = os.path.dirname(os.path.abspath(__file__))


def main():

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
        ["id3", "has", "id5"],
        ["id1", "has", "id6"],
        ["id6", "has", "id7"],
    ]:
        A.new_relation(fromid, toid, relation)

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
        ["id3", "has", "id5"],
        ["id1", "has", "id6"],
        ["id6", "has", "id7"],
    ]:
        B.new_relation(fromid, toid, relation)

    # Now let's generate a basic diff
    c = Difference(A, B, namespaceA="A", namespaceB="B")
    c.run()

    # We can also provide an example logic program!
    lp = os.path.join(here, "show-uniques.lp")
    res = c.run(lp)
    print(res)


if __name__ == "__main__":
    main()
