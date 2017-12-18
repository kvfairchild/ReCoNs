from __future__ import division
import numpy as np

from .link import Link
from .node import node_factory
from .nodenet import Nodenet


# NODES

def generate_node_data(symbol_array):
	num_ops = (len(symbol_array)-1)/2 # number of operations in function

	node_list = []

	for layer_index in range(0, len(symbol_array)):
		if layer_index % 2 == 0 and layer_index != len(symbol_array)-1:
			node_list.append([["layer"+str(layer_index)+"ops_node", "recon"]])
		elif layer_index % 2 != 0:
			node_list.append([["layer"+str(layer_index)+"node"+str(n), "recon"]
			for n in range(0, 3)])
		else:
			node_list.append([["layer"+str(layer_index)+"node"+str(n), "recon"]
			for n in range(0, int((num_ops*2)+num_ops))])

	return node_list

def add_nodes(recon, node_data):
	recon.add_layers(node_factory(node_data, "recon"))

def remove_nodes(recon, node_data):
	node_dict = recon.node_dict
	[node_dict.pop(name) for name in node_data]


# LINKS

def generate_link_data(recon, symbol_array):
	num_ops = (len(symbol_array)-1)/2 # number of operations in function

	link_list = []

	for layer_index, layer in enumerate(recon.layers):
		if layer_index % 2 == 0 and layer_index != len(symbol_array)-1:
			sub_links = [{"origin": [origin_node.name, "sub"], "target": [target_node.name, "sub"]} 
			for origin_node in layer for target_node in recon.layers[layer_index+1]]
			sur_links = [{"origin": [origin_node.name, "sur"], "target": [target_node.name, "sur"]} 
			for origin_node in layer for target_node in recon.layers[layer_index+1]]
			link_list.append([sub_links, sur_links])
		elif layer_index % 2 != 0 and layer_index != len(symbol_array)-2:
			sub_links = [{"origin": [origin_node.name, "sub"], "target": [target_node.name, "sub"]} 
			for origin_index, origin_node in enumerate(layer) 
			for target_node in recon.layers[layer_index+1] if origin_index == 0]
			sur_links = [{"origin": [origin_node.name, "sur"], "target": [target_node.name, "sur"]} 
			for origin_index, origin_node in enumerate(layer) 
			for target_node in recon.layers[layer_index+1] if origin_index == 0]
			por_links = [{"origin": [origin_node.name, "por"], "target": [target_node.name, "por"]} 
			for origin_index, origin_node in enumerate(layer) for target_index, target_node in enumerate(layer)
			if origin_index + 1 == target_index]
			ret_links = [{"origin": [origin_node.name, "ret"], "target": [target_node.name, "ret"]} 
			for origin_index, origin_node in enumerate(layer) for target_index, target_node in enumerate(layer)
			if origin_index + 1 == target_index]
			link_list.append([sub_links, sur_links, por_links, ret_links])
		elif layer_index == len(symbol_array)-2:
			por_links = [{"origin": [origin_node.name, "por"], "target": [target_node.name, "por"]} 
			for origin_index, origin_node in enumerate(layer) for target_index, target_node in enumerate(layer)
			if origin_index + 1 == target_index]
			ret_links = [{"origin": [origin_node.name, "ret"], "target": [target_node.name, "ret"]} 
			for origin_index, origin_node in enumerate(layer) for target_index, target_node in enumerate(layer)
			if origin_index + 1 == target_index]
			link_list.append([por_links, ret_links])
		else: # last layer "leaf-node" links
			sub_links = []
			sur_links = []

			i = layer_index-1
			j = 0
			while j < len(layer):
				target_layer = recon.layers[i]
				for target_index, target_node in enumerate(layer):
					for origin_index, origin_node in enumerate(target_layer):
						if target_index == origin_index + j:
							sub_links.append({"origin": [origin_node.name, "sub"], "target": [target_node.name, "sub"]})
							sur_links.append({"origin": [origin_node.name, "sur"], "target": [target_node.name, "sur"]})
				i -= 2 # only odd-indexed layers
				j += len(recon.layers[i])

			link_list.append([sub_links, sur_links])

	return link_list

def link_nodes(recon, link_data):

	recon.links_list = [[(_create_link(recon, link)) 
	for sub_layer in layer for link in sub_layer] for layer in link_data]

def _create_link(recon, link_data):
	origin_node = recon.node_dict[link_data.get("origin")[0]]
	origin_gate = origin_node.get_gate(link_data.get("origin")[1])
	target_node = recon.node_dict[link_data.get("target")[0]]
	target_slot = target_node.get_slot(link_data.get("target")[1])
	weight = 1

	return Link(origin_node, origin_gate, target_node, target_slot, weight)
