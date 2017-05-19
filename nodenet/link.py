import uuid
import random

class Link:
	def __init__(self, origin_node, gate, target_node, slot, weight):
		self.uuid = uuid.uuid()
		self.origin_node = origin_node
		self.gate = gate
		self.target_node = target_node
		self.slot = slot
		self.weight = random()
