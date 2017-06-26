from math import tanh

class Gate:
    def __init__(self, name, activation, parameters=None, gate_function=None):
        self.name = name
        self.activation = activation
        self.parameters = parameters if parameters else {}
        self.gate_function = gate_function if gate_function else self._default_gate_function

    def _default_gate_function(self, activation):
        self.activation = tanh(activation)

    def is_active(self):
    	return self.activation > self.parameters.get("threshold")
