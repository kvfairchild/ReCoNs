from .link import Link
from .node_factory import node_factory
from .nodenet import Nodenet

def add_nodes(nodenet, nodes_list):
	nodenet.add_nodes(node_factory(nodes_list))

def remove_nodes(nodenet, nodes_list):
	node_dict = nodenet.node_dict

	for name in nodes_list:
		node_dict.pop(name)

def link_nodes(nodenet, links_list):
	for link in links_list:
		nodenet.add_link(create_link(nodenet, link))

def create_link(nodenet, link_data):
	origin_node = nodenet.node_dict[link_data.get("origin")[0]]
	origin_gate = origin_node.get_gate(link_data.get("origin")[1])
	target_node = nodenet.node_dict[link_data.get("target")[0]]
	target_slot = target_node.get_slot(link_data.get("target")[1])
	
	return Link(origin_node, origin_gate, target_node, target_slot)

def initialize_root_node(nodenet, activation, node_name, slot_name):
	root_node = nodenet.node_dict[node_name]
	root_slot = root_node.get_slot(slot_name)

	if activation >= 0:
		root_slot.activation = activation
	else:
		raise ValueError

def set_exit_node(nodenet, node_name, gate_name):
	nodenet.exit_node_list = [node_name, gate_name]

def generate_node_data(num_nodes):
	return [["register"+str(n+1), "register"] for n in range(0, num_nodes)] + [["root_node", "register"]] + [["exit_node", "register"]]

