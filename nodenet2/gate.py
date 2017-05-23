from math import tanh
from uuid import uuid4


"""
The activation is meant to be the current value, not the threshold value.
You can define a threshold value as a parameter later, and do the thresholding in the gate function.
"""


class Gate:
    def __init__(self, name, activation, parameters=None, gate_function=None):
        self.uid = uuid4()  # the gate is uniquely defined by its parent node and index, so uid is waste of memory.
        self.name = name
        self.activation = activation
        self.current_value = None
        """
        you cannot init the parameters with {} in the function definition because {} is mutable. So, lets use
        "None" in the definition and fix it here.
        """
        self.parameters = parameters if parameters else {}
        self.gate_function = gate_function if gate_function else self._default_gate_function

    """
    The naming convention suggests only a single underline for private functions. Double underlines are for system
    symbols are comparable libraries.
    """
    def _default_gate_function(self, input_value):
        self.current_value = tanh(input_value)

    def is_active(self):
        return self.current_value >= self.activation


