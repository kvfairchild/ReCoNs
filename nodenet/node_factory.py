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
        nodes = []
        for node in nodes_list:
            node_data = get_slots_and_gates(*NODE_TYPES.get(node[1]))
            nodes.append(Node(node[0], *node_data))
        return nodes
    # return default node
    else:
        return Node(*NODE_TYPES.get("register"))

def get_slots_and_gates(slot_names, gate_names):
    return [
        slot_factory(slot_names),
        gate_factory(gate_names)
    ]