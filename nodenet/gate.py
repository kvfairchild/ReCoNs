from math import tanh
import numpy as np

GATE_TYPES = {
    "gen": [
        "gen",
        0,
        {"threshold": -2}
    ],
    "por": [
        "por",
        0,
        {"threshold": -2}
    ],
    "ret": [
        "ret",
        0,
        {"threshold": -2}
    ],
    "sub": [
        "sub",
        0,
        {"threshold": -2}
    ],
    "sur": [
        "sur",
        0,
        {"threshold": -2}
    ],
    "cat": [
        "cat",
        0,
        {"threshold": 0.1}
    ],
    "exp": [
        "exp",
        0,
        {"threshold": 0.2}
    ],
    "sym": [
        "sym",
        0,
        {"threshold": 0.3}
    ],
    "ref": [
        "ref",
        0,
        {"threshold": 0.4}
    ]
}


def gate_factory(gate_names, is_output_node):
    # return a list of gates, generated from gate types based on a list of names
    if is_output_node == False:
        return [Gate(*GATE_TYPES.get(name) + ["default"]) for name in gate_names]
    else: 
        return [Gate(*GATE_TYPES.get(name) + ["output"]) for name in gate_names]

class Gate:
    def __init__(self, name=None, activation=None, parameters=None, gate_function=None):
        self.name = name
        self.activation = activation if activation is not None else 0
        self.parameters = parameters if parameters else {}
        self.gate_function = {
			"default": self._default_gate_function,
			"output": self._output_gate_function
		}[gate_function] if gate_function is not None else self._default_gate_function

    def _default_gate_function(self, activation):
    	self.activation = tanh(activation)

    def _output_gate_function(self, activation):
    	self.activation = activation

    def is_active(self):
        return self.activation > self.parameters.get("threshold")
