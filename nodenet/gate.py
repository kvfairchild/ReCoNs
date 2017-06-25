from math import tanh
from uuid import uuid4

class Gate:
    def __init__(self, name, activation, parameters=None, gate_function=None):
        self.uid = uuid4()  # the gate is uniquely defined by its parent node and index, so uid is waste of memory.
        self.name = name
        self.activation = activation
        self.current_value = None
        self.parameters = parameters if parameters else {}
        self.gate_function = gate_function if gate_function else self._default_gate_function

    def _default_gate_function(self, input_value):
        self.current_value = tanh(input_value)

    def is_active(self):
        return self.current_value >= self.activation
