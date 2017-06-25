from .node import Node
from .gate_factory import gate_factory
from .slot_factory import slot_factory

NODE_TYPES = {
    "register": [
        slot_factory([ "gen" ]),
        gate_factory([ "gen" ])
    ],
    "sensor": [
        slot_factory([ "gen" ])
    ],
    "actuator": [
        slot_factory([ "gen" ])
    ],    
    "concept": [
        slot_factory([ "gen" ]),
        gate_factory([ "gen", "por", "ret", "sub", "sur", "cat", "exp", "sym", "ref" ])
    ]
}

def node_factory(nodes_list):
    # return a list of gates, generated from gate types based on a list of names
    if len(nodes_list) > 0:
        return [Node(node[0], *NODE_TYPES.get(node[1])) for node in nodes_list]
    # return default
    else:
        return Node(*NODE_TYPES.get("register"))
