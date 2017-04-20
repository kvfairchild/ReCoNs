import uuid

from .slot import Slot

class Node:
	def __init__(self, name = None, slot_vector = "gen", gate_vector = "gen", node_function = None):
		self.uuid = uuid.uuid4()
		self.name = name if name != None else self.uuid
		self.slot_vector = [ slot_vector ]
		self.gate_vector = [ gate_vector ]
		self.node_function = node_function if node_function != None else __default_node_function()

	def __default_node_function():
		return None