from .link import Link
from .node_factory import node_factory
from .nodenet import Nodenet

def add_nodes(nodes_list):
	Nodenet.Instance().add_nodes(node_factory(nodes_list))

def link_nodes(links_list):
	for link in links_list:
		create_link(link)

def create_link(link_data):
	origin_node = Nodenet.Instance().node_dict[link_data.get("origin")[0]]
	origin_gate = origin_node.get_gate(link_data.get("origin")[1])
	target_node = Nodenet.Instance().node_dict[link_data.get("target")[0]]
	target_slot = target_node.get_gate(link_data.get("target")[1])
	
	return Link(origin_node, origin_gate, target_node, target_slot)

# def build_nodenet(self):
#     for layer in range(0, self.num_layers):
#     	layer = __build_layer()
#     	self.node_net.append(layer)
#     __link_nodenet(node_net)

# def __link_nodenet(self):
# 	# iterate through n-1 layers for origin nodes
# 	for layer_index in range(0, self.num_layers-1):
# 		for node_index in range(0, len(self.node_net[layer_index])):
# 			self.__create_link(self.node_net[layer_index][node_index], self.node_net[layer_index+1])

# def __create_link(self, origin_node, target_layer):
# 	for target_node in target_layer:
# 		for target_slot in target_node.slot_vector:
# 			self.link_list.append(self.__link_factory(origin_node, origin_node.gate_vector[0], target_node, target_slot))

# def __remove_node(self, name):
# 	self.node_dict.pop(name, None) 

# def __link_factory(self, origin_node, origin_gate, target_node, target_slot):
# 	link = Link(origin_node, origin_gate, target_node, target_slot)
# 	return link
