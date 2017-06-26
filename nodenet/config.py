from .link import Link
from .node_factory import node_factory
from .nodenet import Nodenet

def add_nodes(nodes_list):
	Nodenet.Instance().add_nodes(node_factory(nodes_list))

def remove_nodes(nodes_list):
	node_dict = Nodenet.Instance().node_dict

	for node in nodes_list:
		node_dict.pop(node)

def link_nodes(links_list):
	for link in links_list:
		Nodenet.Instance().add_link(create_link(link))
	print Nodenet.Instance().links_list

def create_link(link_data):
	origin_node = Nodenet.Instance().node_dict[link_data.get("origin")[0]]
	origin_gate = origin_node.get_gate(link_data.get("origin")[1])
	target_node = Nodenet.Instance().node_dict[link_data.get("target")[0]]
	target_slot = target_node.get_gate(link_data.get("target")[1])
	
	return Link(origin_node, origin_gate, target_node, target_slot)
