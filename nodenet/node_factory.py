from .node import Node
from .gate_factory import gate_factory
from .slot_factory import slot_factory

NODE_TYPES = {
    "register": [
        [ "gen" ],
        [ "gen" ]
    ],
    "sensor": [
        [ "gen" ]
    ],
    "actuator": [
        [ "gen" ]
    ],    
    "concept": [
        [ "gen" ],
        [ "gen", "por", "ret", "sub", "sur", "cat", "exp", "sym", "ref" ]
    ]
}

def node_factory(nodes_list):
    # return a list of nodes, generated from node types based on a list of names
    if len(nodes_list) > 0:
        return [Node(node[0], *get_slots_and_gates(*NODE_TYPES.get(node[1]))) for node in nodes_list]
    else:
        raise ValueError("please pass in node data or number of nodes to create")

def get_slots_and_gates(slot_names, gate_names):
    return [
        slot_factory(slot_names),
        gate_factory(gate_names)
    ]
