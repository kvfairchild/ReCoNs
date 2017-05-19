import uuid

from .node import Node
from .link import Link
from .gate import Gate
from .slot import Slot

class Nodenet:
	def __init__(self, name = None, num_layers = None, num_nodes = None):
		self.uid = uuid.uuid4()
		self.name = name
		self.num_layers = num_layers
		self.num_nodes = num_nodes
		self.node_dict = {}
		self.slot_dict = {}
		self.gate_dict = {}

	def node_factory(self, name = None, slot_vector = None, gate_vector = None, node_function = None):
		node = Node(name, slot_vector, gate_vector, node_function)
		self.node_dict[node.name] = node
		return node

	def remove_node(self, name):
		self.node_dict.pop(name, None) 

	def link_factory(self, origin_node, origin_gate, target_node, target_slot):
		link = Link(origin_node, origin_gate, target_node, target_slot)
		return link

	def build_nodenet(self):
	    node_net = []
	    for n in range(0, self.num_layers):
	    	node_net.append(self.build_layer())
	    self.link_nodenet(node_net)
	    return node_net

	def build_layer(self):
	    layer = []
	    for n in range(0, self.num_nodes):
	        layer.append(self.node_factory(name = None, slot_vector = None, gate_vector = None, node_function = None))
	    return layer

	def link_nodenet(self, node_net):
		origin_nodes = []
		for n in range(0, self.num_layers-1):
		 	for n in node_net[n]:
		 		origin_node = n.name
		 		target_nodes = []
		 		for n in next(node_net[n]):
		 			target_nodes.append(n.name)
		 		origin_nodes.append(n.name, target_nodes)


		# 		origin_node = n.name
		# 		for n in n.gate_vector:
		# 			origin_gate = n.name
		# 		origins.append([origin_node, origin_gate])
		# # get target nodes and slots
		# for n in range(1, self.num_layers):
		# 	for n in node_net[n]:
		# 		target_node = n.name
		# 		for n in n.slot_vector:
		# 			target_slot = n.name
		# 		targets.append([target_node, target_slot])
	# 	# # create links from all origin gates to all target slots				
	# 	self.create_links(origins, targets)

	# def create_links(self, origins, targets):
	# 	links = []
	# 	for n in origins:
	# 		origin_node = n[0]
	# 		origin_gate = n[1]
	# 	for n in targets
	# 		target_node = n[0]
	# 		target_slot = n[1]
			#links.append(self.link_factory(origin_node, origin_gate, target_node, target_slot))