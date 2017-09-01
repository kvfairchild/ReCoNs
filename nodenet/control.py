from .nodenet import Nodenet

import numpy as np

def run(nodenet):
	return _step_function(nodenet)
 
def _step_function(nodenet):
    output = []

    for i, layer in enumerate(nodenet.layers):
        _net_function(nodenet)
        _link_function(nodenet)

        # fetch output from last layer
        if i == len(nodenet.layers)-1:
            for node in nodenet.layers[i]:
                for gate in node.gate_vector:
                	normal_output = gate.activation / (28*28) # normalize output
                	output.append(normal_output)

        _zero_gates(nodenet)

    return _softmax(output)

# call node function for nodes that received activation
def _net_function(nodenet):
	node_dict = nodenet.node_dict

	for node in node_dict.values():
		for slot in node.slot_vector:
			if slot.activation > 0:
				node.node_function(slot.activation)
				slot.activation = 0

# multiply active node gate values with link weights, sum in target slots
def _link_function(nodenet):
	for link in nodenet.links_list:
		if link.origin_gate.is_active():
			_send_activation_to_target_slot(link)

# HELPER FUNCTIONS
def _zero_gates(nodenet):
	for link in nodenet.links_list:
		if link.origin_gate.activation > 0:
			link.origin_gate.activation = 0

def _send_activation_to_target_slot(link):
	activation = link.origin_gate.activation * link.weight
	link.target_slot.activation = link.target_slot.activation + activation

def _is_exit_node(nodenet, link):
	return link.target_node.name == nodenet.exit_node_list[0]\
	and link.target_slot.name == nodenet.exit_node_list[1]

def _softmax(normal_output):
	exp_normal_output = np.exp(normal_output - np.max(normal_output))
	return exp_normal_output / exp_normal_output.sum()

