import uuid

class Nodenet:

	def __init__ (self, name = None):
		self.uuid = uuid.uuid()
		self.name = name

	