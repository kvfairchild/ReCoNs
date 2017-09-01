from .link import Link
from .node_factory import node_factory
from .nodenet import Nodenet

# NODES

def generate_node_data(network_dimensions):
	node_data = []
	for layer_index, num_nodes in enumerate(network_dimensions):
		layer = [["layer"+str(layer_index)+"node"+str(n), "register"] for n in range(0, num_nodes)]
		node_data.append(layer)
	return node_data

def add_nodes(nodenet, node_data):
	nodenet.add_nodes(node_factory(node_data))

def remove_nodes(nodenet, node_data):
	node_dict = nodenet.node_dict

	for name in node_data:
		node_dict.pop(name)

# LINKS

def generate_link_data(node_data):
	link_data = []
	for target_node in node_data[1]:
	 	for origin_node in node_data[0]:
	 		link = {"origin": [origin_node[0], "gen"], "target": [target_node[0], "gen"]}
	 		link_data.append(link)
	return link_data

def link_nodes(nodenet, link_data):
	for link in link_data:
		nodenet.add_link(create_link(nodenet, link))

def create_link(nodenet, link_data):
	origin_node = nodenet.node_dict[link_data.get("origin")[0]]
	origin_gate = origin_node.get_gate(link_data.get("origin")[1])
	target_node = nodenet.node_dict[link_data.get("target")[0]]
	target_slot = target_node.get_slot(link_data.get("target")[1])

	return Link(origin_node, origin_gate, target_node, target_slot)

# INITIALIZE NETWORK

def initialize_root_node(nodenet, activation, node_name, slot_name):
	root_node = nodenet.node_dict[node_name]
	root_slot = root_node.get_slot(slot_name)

	if activation >= 0:
		root_slot.activation = activation
	else:
		raise ValueError

def set_exit_node(nodenet, node_name, gate_name):
	nodenet.exit_node_list = [node_name, gate_name]
