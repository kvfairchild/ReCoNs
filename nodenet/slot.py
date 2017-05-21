from uuid import uuid4

class Slot:
	def __init__(self, name, activation):
		self.uid = uuid4()
		self.name = name
		self.activation = activation if activation != None else slots.get(name, default=None)
		self.current_value = 0
