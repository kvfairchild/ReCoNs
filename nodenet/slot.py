class Slot:
	def __init__(self, name, activation):
		self.name = name
		self.activation = activation if activation != None else slots.get(name, default=None)