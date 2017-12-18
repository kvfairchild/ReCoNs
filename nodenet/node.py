from uuid import uuid4
from .slot import slot_factory
from .gate import gate_factory

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
    ],
    "recon": [
        [ "gen", "por", "ret", "sub", "sur" ],
        [ "gen", "por", "ret", "sub", "sur"]
    ]
}

def node_factory(node_data, net_type):
# return a list of nodes, generated from node types based on a list of names
    if len(node_data) > 0:
        layers = []
        for layer_index, layer in enumerate(node_data):
            if net_type == "nodenet":
                if layer_index < len(node_data)-1:
                    node = [Node(node[0], *_get_slots_and_gates(*NODE_TYPES.get(node[1]))) for node in layer]
                    layers.append(node)
                else:
                    node = [Node(node[0], *_get_output_slots_and_gates(*NODE_TYPES.get(node[1]))) for node in layer]
                    layers.append(node)
            elif net_type == "recon":
                    node = [Node(node[0], *_get_slots_and_gates(*NODE_TYPES.get(node[1]))) for node in layer]
                    layers.append(node)
            else:
                raise ValueError("net type not recognized")
        return layers
    else:
        raise ValueError("please pass in node data or number of nodes to create")

class Node:
    def __init__(self, name=None, slot_vector=None, gate_vector=None, node_function=None, activation=0):
        self.uid = uuid4()
        self.name = name
        self.node_function = node_function if node_function is not None else self._default_node_function
        self.slot_vector = slot_vector
        self.gate_vector = gate_vector
        self.activation = activation

    @property
    def name(self):
        return self.name if self.name else self.uid

    @name.setter
    def name(self, value):
        self.name = value

    def get_slot(self, name):
        for slot in self.slot_vector:
            if name == slot.name:
                return slot

    def get_gate(self, name):
        for gate in self.gate_vector:
            if name == gate.name:
                return gate
                
    def _default_node_function(self, activation):
    # calls all gate functions, passes value from slot
        for gate in self.gate_vector:
            gate.gate_function(activation)


# NODE FACTORY HELPERS

def _get_slots_and_gates(slot_names, gate_names):
    return [
        slot_factory(slot_names),
        gate_factory(gate_names, is_output_node=False)
    ]

def _get_output_slots_and_gates(slot_names, gate_names):
    return [
        slot_factory(slot_names),
        gate_factory(gate_names, is_output_node=True)
    ]
