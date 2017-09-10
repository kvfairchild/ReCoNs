from __future__ import division

from .link import Link
from .node_factory import node_factory
from .nodenet import Nodenet

# NODES

def generate_node_data(network_dimensions):
	return [[["layer"+str(layer_index)+"node"+str(n), "register"] 
	for n in range(0, num_nodes)] for layer_index, num_nodes in enumerate(network_dimensions)]

def add_nodes(nodenet, node_data):
	nodenet.add_layers(node_factory(node_data))

def remove_nodes(nodenet, node_data):
	node_dict = nodenet.node_dict
	[node_dict.pop(name) for name in node_data]

# LINKS

def generate_link_data(nodenet):
	return [[[{"origin": [origin_node.name, "gen"], "target": [target_node.name, "gen"]} 
	for origin_node in nodenet.layers[layer_index-1]] for target_node in layer] 
	for layer_index, layer in enumerate(nodenet.layers) if 0 < layer_index < len(nodenet.layers)]

def link_nodes(nodenet, link_data):
	nodenet.links_list = [[[(create_link(nodenet, link)) 
	for link in node] for node in layer] for layer in link_data]

def create_link(nodenet, link_data):
	origin_node = nodenet.node_dict[link_data.get("origin")[0]]
	origin_gate = origin_node.get_gate(link_data.get("origin")[1])
	target_node = nodenet.node_dict[link_data.get("target")[0]]
	target_slot = target_node.get_slot(link_data.get("target")[1])

	return Link(origin_node, origin_gate, target_node, target_slot)

# PREPARE DATA AND SET ACTIVATION

def _flatten_image(image):
	return [pixel for row in image for pixel in row]
			
def set_activation(nodenet, image):
	flattened_image = _flatten_image(image)

	activation = []

	for i, node in enumerate(nodenet.layers[0]):

		for pixel in flattened_image[i]:

			pixel = pixel * (1/255) # normalize values between [0,1]
			slot = node.get_slot("gen")
			slot.activation = pixel

			activation.append(slot.activation)

	return activation

# UPDATE LINK WEIGHTS

def update_weights(nodenet, activation, error_array, image_index):
	output_links = nodenet.links_list[len(nodenet.layers)-2]
	INITIAL_LEARNING_RATE = .05
	RATE_DECAY = .0001
	global learning_rate

	# set and decay learning rate 
	learning_rate = INITIAL_LEARNING_RATE if image_index == 0 else _decay_learning_rate(learning_rate, RATE_DECAY)
		
	# set weights for each link to output nodes based on pixel value
	for node_index, output_node in enumerate(output_links):

		for i in range(len(activation)):
			link = output_node[i]
			link.weight += learning_rate * activation[i] * error_array[node_index]

def _decay_learning_rate(learning_rate, RATE_DECAY):
	learning_rate = learning_rate * (learning_rate / (learning_rate + (learning_rate * RATE_DECAY)))
	
	return learning_rate
