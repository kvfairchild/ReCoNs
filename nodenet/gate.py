from math import tanh
from uuid import uuid4

class Gate:
	def __init__(self, name, activation, parameters = {}, gate_function = None):
		self.uid = uuid4()
		self.name = name
		self.activation = activation
		self.current_value = None
		self.parameters = parameters
		self.gate_function = gate_function if gate_function != None else self.__default_gate_function

	def __default_gate_function(self, input_value):
		self.current_value = tanh(input_value)

	def is_active(self):
		return self.current_value >= self.activation
