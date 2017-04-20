class Gate:
	def __init__(self, name, activation, parameters = {}, gate_function = None):
		self.name = name
		self.activation = activation
		self.parameters = parameters
		self.gate_function = gate_function
