from .node import Node
from .gate_factory import gate_factory
from .slot_factory import slot_factory

NODE_TYPES = {
    "sensor": [
        "sensor",
        gate_factory([ "por", "gen"]),
        slot_factory(["por"])
    ],
    "concept": [
        "concept"
    ],
    "register": [
        "register"
    ],
}

def node_factory(node_names):
    # return a list of gates, generated from gate types based on a list of names
    if len(node_names) > 0:
        return [Node(*NODE_TYPES.get(name)) for name in node_names]
    # return default
    else:
        return Node(*NODE_TYPES.get("sensor"))
