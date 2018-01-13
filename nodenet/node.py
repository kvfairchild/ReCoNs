from uuid import uuid4

from .gate import gate_factory
from .slot import slot_factory

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
        [ "gen", "por", "ret", "sub", "sur" ]
    ]
}

# return a list of nodes, generated from a list of node names and types
def node_factory(node_data, net_type):
    if len(node_data) > 0:
        layers = []
        for layer_index, layer in enumerate(node_data):
            if net_type == "nodenet":
                if layer_index < len(node_data)-1:
                    nodes = [Node(node[0], *_get_slots_and_gates(*NODE_TYPES.get(node[1]))) for node in layer]
                    layers.append(nodes)
                else:
                    nodes = [Node(node[0], *_get_output_slots_and_gates(*NODE_TYPES.get(node[1]))) for node in layer]
                    layers.append(nodes)
            elif net_type == "recon":
                if layer_index < len(node_data)-1 and layer_index != 1:
                    nodes = [Node(node[0], *_get_output_slots_and_gates(*NODE_TYPES.get(node[1]))) for node in layer]
                    layers.append(nodes)
                # create layer 1 "equals node" as action node
                elif layer_index == 1:
                    nodes = []
                    for node_index, node in enumerate(layer):
                        if node_index != layer[len(layer)-1]:
                            nodes.append(Node(node[0], *_get_output_slots_and_gates(*NODE_TYPES.get(node[1]))))
                        else:
                            nodes.append(ActionNode(node[0], *_get_output_slots_and_gates(*NODE_TYPES.get(node[1]))))
                    layers.append(nodes)
                # create all last-layer nodes as action nodes
                else:
                    nodes = [ActionNode(node[0], *_get_output_slots_and_gates(*NODE_TYPES.get(node[1]))) for node in layer]
                    layers.append(nodes)
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

    # calls all gate functions, passes value from slot            
    def _default_node_function(self, activation):
        for gate in self.gate_vector:
            gate.gate_function(activation)

class ActionNode(Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        self.value = kwargs.pop("value") if "value" in kwargs else None

    def push_to_stack(self, stack):
        if self.activation > 0 and self.value is not None:
            stack.push(self.value)

    def pull_from_stack(self, stack):
        if self.activation > 0 and self.value is None:
            self.value = stack.pop()


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
