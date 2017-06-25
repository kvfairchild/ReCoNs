from uuid import uuid4

class Nodenet:
	def __init__(self, name = None, num_layers = None, num_nodes = None):
		self.uid = uuid4()
		self.name = name
		self.num_layers = num_layers
		self.num_nodes = num_nodes
		self.node_net = []
		self.node_dict = {}
		self.link_list = []
