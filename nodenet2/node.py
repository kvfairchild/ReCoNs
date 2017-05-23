from uuid import uuid4

from slot import Slot
from gate import Gate
from gate_types import GATE_TYPES



"""
Theoretically, the slots and gates should have been passed in here directly...
"""


class Node:
    def __init__(self, name=None, slot_names=None, gate_names=None, node_function=None):
        self.uid = uuid4()
        self.name = name  # introduced getter and setter below, so we don't store the UID twice
        self.node_function = node_function if node_function is not None else self._default_node_function
        self.current_value = None

        if slot_names is None:
            slot_names = ["gen"]
        self.slot_vector = [Slot(name) for name in slot_names]  # using a list comprehension for clarity and speed
        if gate_names is None:
            gate_names = ["gen"]
        self.gate_vector = [Gate(*GATE_TYPES.get(name)) for name in gate_names]

    @property
    def name(self):
        return self.name if self.name else self.uid

    @name.setter
    def name(self, value):
        self.name = value

    def _default_node_function(self):
        """calls all gate functions, passes value from slot"""
        for gate in self.gate_vector:
            gate.gate_function(self.current_value)

