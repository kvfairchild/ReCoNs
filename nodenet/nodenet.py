import uuid

from .node import Node
from .link import Link

class Nodenet:
	def __init__(self, name = None, num_layers = None, num_nodes = None):
		self.uid = uuid.uuid4()
		self.name = name
		self.num_layers = num_layers
		self.num_nodes = num_nodes
		self.node_dict = {}
		self.slot_dict = {}
		self.gate_dict = {}

	def node_factory(self, name = None, slot_vector = None, gate_vector = None, node_function = None):
		node = Node(name, slot_vector, gate_vector, node_function)
		self.node_dict[node.name] = node
		return node

	def remove_node(self, name):
		self.node_dict.pop(name, None) 

	def link_nodes(self, num_layers, num_nodes):
		num_layers = num_layers
		num_nodes = num_nodes
		print num_layers
		print num_nodes