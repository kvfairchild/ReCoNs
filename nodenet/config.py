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

# PREPARE DATA AND SET ACTIVATION

def _flatten_image(image):
	flattened = []
	for row in image:
		for pixel in row:
			flattened.append(pixel)
	return flattened
			
def set_activation(nodenet, image):
	flattened_image = _flatten_image(image)

	for i, node in enumerate(nodenet.layers[0]):

		for pixel in flattened_image[i]:
			slot = node.get_slot("gen")
			slot.activation = pixel

# UPDATE LINK WEIGHTS

def update_weights(nodenet, error_array, image, i):

	flattened_image = _flatten_image(image)
	output_links = _get_output_links(nodenet)
	INITIAL_LEARNING_RATE = .05
	RATE_DECAY = .0001
	global learning_rate

	# set learning weight
	if i == 0:
		learning_rate = INITIAL_LEARNING_RATE
	else:
		learning_rate = _decay_learning_rate(learning_rate, RATE_DECAY)
		
	# set weights for each link to output nodes based on pixel value
	for node_index, node_links in enumerate(output_links):
			
		i = 0

		while i < len(flattened_image):

			for link in node_links:
				pixel = flattened_image[i][0]
	   			link.weight += learning_rate * pixel * error_array[node_index]
	   			i += 1

# LINK WEIGHT HELPER FUNCTIONS

def _decay_learning_rate(learning_rate, RATE_DECAY):

	learning_rate = learning_rate * (learning_rate / (learning_rate + (learning_rate * RATE_DECAY)))
	
	return learning_rate

def _get_output_links(nodenet):
	output_links = []

	for node in nodenet.layers[len(nodenet.layers)-1]:
		for slot in node.slot_vector:
			output_links.append(_get_link_by_target_slot(nodenet, slot))

	return output_links

def _get_link_by_target_slot(nodenet, slot):

	node_input_links = []

	for link in nodenet.links_list:
		if slot == link.target_slot:
			node_input_links.append(link)
	
	return node_input_links
