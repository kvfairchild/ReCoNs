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
	    self.create_links(node_net)
	    return node_net

	def build_layer(self):
	    layer = []
	    for n in range(0, self.num_nodes):
	        layer.append(self.node_factory(name = None, slot_vector = None, gate_vector = None, node_function = None))
	    return layer

	def create_links(self, node_net):
		links = []
		# get origin node and gate
		print "origin nodes"
		for n in range(0, self.num_layers-1):
			for n in node_net[n]:
				origin_node = n.name
				print origin_node
				for n in n.gate_vector:
					origin_gate = n.name
		# get target node and slot
		print "target nodes"
		for n in range(1, self.num_layers):
			for n in node_net[n]:
				target_node = n.name
				print target_node
				for n in n.slot_vector:
					target_slot = n.name
		#establish link between origin and target node
		print "*****"
		for n in range(0, self.num_layers):
			for n in node_net[n]:
				links.append(self.link_factory(origin_node, origin_gate, target_node, target_slot))
		for n in links:
			print n.origin_node, " ", target_node
		return links