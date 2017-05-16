import uuid

from .node import Node
from .link import Link

class Nodenet:
	def __init__(self, name = None):
		self.uid = uuid.uuid4()
		self.name = name
		self.node_dict = {}
		self.slot_dict = {}
		self.gate_dict = {}

	def node_factory(self, name = None, slot_vector = "gen", gate_vector = "gen", node_function = None):
		node = Node(name, slot_vector, gate_vector, node_function)
		self.node_dict[node.name] = node
		return node

	def remove_node(self, name):
		self.node_dict.pop(name, None) 