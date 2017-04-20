import uuid

from .slot import Slot

class Node:

	def __init__ (self, name = None, slot_vector = "gen", gate_vector = "gen", node_function = None):
		self.uuid = uuid.uuid()
		self.name = name
		self.slot_vector = [ slot_vector ]
		self.gate_vector = [ gate_vector ]
		self.node_function = node_function