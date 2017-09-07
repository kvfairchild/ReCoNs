from __future__ import division

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
	nodenet.add_layers(node_factory(node_data))

def remove_nodes(nodenet, node_data):
	node_dict = nodenet.node_dict

	for name in node_data:
		node_dict.pop(name)

# LINKS

def generate_link_data(nodenet):
	link_data = []
	
	for layer_index, layer in enumerate(nodenet.layers):

		# don't need links for the last layer of nodes
		if 0 < layer_index < len(nodenet.layers):
			layer_links = []

		 	for target_node in layer:
		 		node_links = []

		 		for origin_node in nodenet.layers[layer_index-1]:

			 		node_links.append({
			 			"origin": [origin_node.name, "gen"],
			 			"target": [target_node.name, "gen"]
			 		})

				layer_links.append(node_links)
		
			link_data.append(layer_links)

	return link_data

def link_nodes(nodenet, link_data):

	for layer in link_data:
		layer_links = []

		for node in layer:
			node_links = []

			for link in node:
				node_links.append(create_link(nodenet, link))

			layer_links.append(node_links)

		nodenet.links_list.append(layer_links)

def create_link(nodenet, link_data):

	origin_node = nodenet.node_dict[link_data.get("origin")[0]]
	origin_gate = origin_node.get_gate(link_data.get("origin")[1])
	target_node = nodenet.node_dict[link_data.get("target")[0]]
	target_slot = target_node.get_slot(link_data.get("target")[1])

	return Link(origin_node, origin_gate, target_node, target_slot)

# PREPARE DATA AND SET ACTIVATION

def _flatten_image(image):
	flattened = []
	for row in image:
		for pixel in row:
			flattened.append(pixel)
	return flattened
			
def set_activation(nodenet, image):
	flattened_image = _flatten_image(image)
	activation = []

	for i, node in enumerate(nodenet.layers[0]):

		for pixel in flattened_image[i]:

			pixel = pixel * (1/255) 
			slot = node.get_slot("gen")
			slot.activation = pixel

			activation.append(slot.activation)

	return activation

# UPDATE LINK WEIGHTS

def update_weights(nodenet, activation, error_array, i):

	output_links = nodenet.links_list[len(nodenet.layers)-2]
	INITIAL_LEARNING_RATE = .05
	RATE_DECAY = .0001
	global learning_rate

	# set and decay learning rate 
	if i == 0:
		learning_rate = INITIAL_LEARNING_RATE
	else:
		learning_rate = _decay_learning_rate(learning_rate, RATE_DECAY)
		
	# set weights for each link to output nodes based on pixel value
	for node_index, output_node in enumerate(output_links):

		i = 0
		while i < (28*28):

			for link in output_node:

			 	pixel = activation[i]
			 	link.weight += learning_rate * pixel * error_array[node_index]
			 	i += 1

def _decay_learning_rate(learning_rate, RATE_DECAY):
	learning_rate = learning_rate * (learning_rate / (learning_rate + (learning_rate * RATE_DECAY)))
	
	return learning_rate
