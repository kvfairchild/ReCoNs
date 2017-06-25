from .node import Node
from .gate_factory import gate_factory
from .slot_factory import slot_factory

NODE_TYPES = {
    "register": [
        "register",
        slot_factory([ "gen" ]),
        gate_factory([ "gen" ])
    ],
    "sensor": [
        "sensor",
        slot_factory([ "gen" ])
    ],
    "actuator": [
        "actuator",
        slot_factory([ "gen" ])
    ],    
    "concept": [
        "concept",
        slot_factory([ "gen" ]),
        gate_factory([ "gen", "por", "ret", "sub", "sur", "cat", "exp", "sym", "ref" ])
    ]
}

def node_factory(node_names):
    # return a list of gates, generated from gate types based on a list of names
    if len(node_names) > 0:
        return [Node(*NODE_TYPES.get(name)) for name in node_names]
    # return default
    else:
        return Node(*NODE_TYPES.get("register"))
