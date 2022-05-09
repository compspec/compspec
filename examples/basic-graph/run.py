from compspec.graph import Graph
from compspec.runner import Composition
import json
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

    # Here is the output in dict form
    print(json.dumps(A.to_dict(), indent=4))

    # Now let's generate asp facts! This is without a logic program
    c = Composition(A, namespace="A")
    c.run()

    # We can also provide an example logic program!
    lp = os.path.join(here, "show-uniques.lp") 
    res = c.run(lp)    
    print(res)


if __name__ == "__main__":
    main()
