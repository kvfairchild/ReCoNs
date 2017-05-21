from uuid import uuid4

from .slot import Slot
from .slot_factory import slot_factory
from .gate_factory import gate_factory

class Node:
	def __init__(self, name = None, slot_vector = None, gate_vector = None, node_function = None):
		self.uid = uuid4()
		self.name = name if name != None else self.uid
		self.slot_vector = slot_factory(["gen"]) if slot_vector is None else slot_factory(slot_vector)
		self.gate_vector = gate_factory(["gen"]) if gate_vector is None else gate_factory(gate_vector)
		self.node_function = node_function if node_function != None else self.__default_node_function
		self.current_value = None

	def __default_node_function(self):
		for gate in self.gate_vector:
			gate.gate_function(self.current_value)
