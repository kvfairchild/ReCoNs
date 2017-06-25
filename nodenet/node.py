from uuid import uuid4

from slot import Slot
from gate import Gate
from gate_factory import GATE_TYPES


class Node:
    def __init__(self, name=None, slot_vector=None, gate_vector=None, node_function=None):
        self.uid = uuid4()
        self.name = name
        self.node_function = node_function if node_function is not None else self._default_node_function
        self.current_value = None
        self.slot_vector = slot_vector
        self.gate_vector = gate_vector

    @property
    def name(self):
        return self.name if self.name else self.uid

    @name.setter
    def name(self, value):
        self.name = value

    def _default_node_function(self):
        #calls all gate functions, passes value from slot
        for gate in self.gate_vector:
            gate.gate_function(self.current_value)
