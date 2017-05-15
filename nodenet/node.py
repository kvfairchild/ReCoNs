import uuid

from .slot import Slot

class Node:
	def __init__(self, name = None, slot = "gen", gate = "gen", node_function = None):
		self.uuid = uuid.uuid4()
		self.name = name if name != None else self.uuid
		self.slot_vector = [ slot ]
		self.gate_vector = [ gate ]
		self.node_function = node_function if node_function != None else self.__default_node_function

	def __default_node_function(self, node_function):
		return None

	def add_slot(self, slot):
		self.slot_vector.append(slot)

	def add_gate(self, gate):
		self.gate_vector.append(gate)