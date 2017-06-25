from uuid import uuid4

from .singleton import Singleton

@Singleton
class Nodenet:
	def __init__(self, name = None):
		self.uid = uuid4()
		self.name = name
		self.node_dict = {}
		self.link_list = []

	def add_nodes(self, nodes):
		for node in nodes:
			self.node_dict[node.name] = node

@property
def name(self):
    return self.name if self.name else self.uid

@name.setter
def name(self, value):
    self.name = value

@property
def node_dict(self, name):
	return self.node_dict[name]
