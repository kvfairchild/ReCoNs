from uuid import uuid4

from node import Node
from link import Link


class Nodenet:
    def __init__(self, name=None, num_layers=None, num_nodes=None):
        self.uid = uuid4()
        self.name = name
        self.num_layers = num_layers
        self.num_nodes = num_nodes
        self.node_net = []
        self.node_dict = {}
        self.link_list = []
        self.slot_dict = {}
        self.gate_dict = {}

    # multiplies active node gate values with link weights, sums them in target slots
    def link_function(self):
        for link in self.link_list:
            if link.origin_gate.is_active():
                current_value = link.origin_gate.current_value * link.weight
                link.target_slot.current_value = link.target_slot.current_value + current_value

    def build_nodenet(self):
        for layer in range(0, self.num_layers):
            layer = self._build_layer()
            self.node_net.append(layer)
        self._link_nodenet()

    def _build_layer(self):
        layer = []
        for node in range(0, self.num_nodes):
            node = self.create_node()
            layer.append(node)
        return layer

    def create_node(self, name=None, slot_name_list=None, gate_name_list=None, node_function=None):
        node = Node(name, slot_name_list, gate_name_list, node_function)
        self.node_dict[node.name] = node
        for slot in node.slot_vector:
            self.slot_dict[slot.uid] = slot
        for gate in node.gate_vector:
            self.gate_dict[gate.uid] = gate
        return node

    def _link_nodenet(self):
        # iterate through n-1 layers for origin nodes
        for layer_index in range(0, self.num_layers - 1):
            for node_index in range(0, len(self.node_net[layer_index])):
                self._create_link(self.node_net[layer_index][node_index], self.node_net[layer_index + 1])

    def _create_link(self, origin_node, target_layer):
        for target_node in target_layer:
            for target_slot in target_node.slot_vector:
                self.link_list.append(
                    self.create_link(origin_node, origin_node.gate_vector[0], target_node, target_slot))

    def _remove_node(self, name):
        self.node_dict.pop(name, None)

    def create_link(self, origin_node, origin_gate, target_node, target_slot):
        link = Link(origin_node, origin_gate, target_node, target_slot)
        return link


"""
The helper methods and build_nodenet are only here to produce a test node net, right? So it makes sense to factor them
out into a file that only calls the public create_node and create_link methods of the nodenet.

Note that you don't provide methods for deletion, and the gates and slots are not maintained in the central data
structure yet. (You need to take care that the nodenet updates whenever you add or remove structure from it.)

"""