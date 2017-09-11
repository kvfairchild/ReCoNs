from __future__ import division
import numpy as np

from .nodenet import Nodenet

def run(nodenet, target_output, i):
		output = _step_function(nodenet) # one hot output
		predicted_int = _one_hot_to_int(output) # integer output
		target_int = _one_hot_to_int(target_output) # integer label
		error_array = target_output - output

		global error_count
		error_count = 0 if i == 0 else error_count

		if predicted_int == target_int:
			print "#", i+1, "prediction: ", predicted_int, " target: ", target_int, "HIT"
		else:
			print "#", i+1, "prediction: ", predicted_int, " target: ", target_int
			error_count += 1
		
		success_rate = "{:.2f}".format((((i+1) - error_count) / (i+1)) * 100)
		print "success rate: ", success_rate, "%"

		return np.array(error_array)
 
def _step_function(nodenet):
    network_output = []

    for i, layer in enumerate(nodenet.layers):
        _net_function(nodenet)
        _link_function(nodenet)
        _zero_gates(nodenet)

        # fetch output from last layer
        if i == len(nodenet.layers)-1:
            for node in nodenet.layers[i]:
                for gate in node.gate_vector:
                	output = gate.activation
                	network_output.append(output)

    return _softmax(network_output) # apply softmax function

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
	for layer in nodenet.links_list:
		for node in layer:
			for link in node:
				if link.origin_gate.is_active():
					_send_activation_to_target_slot(link)

# HELPER FUNCTIONS

def _zero_gates(nodenet):
	for layer in nodenet.links_list:
		for node in layer:
			for link in node:
				if link.origin_gate.activation > 0:
					link.origin_gate.activation = 0

def _send_activation_to_target_slot(link):
	activation = link.origin_gate.activation * link.weight
	link.target_slot.activation = link.target_slot.activation + activation

def _is_exit_node(nodenet, link):
	return link.target_node.name == nodenet.exit_node_list[0]\
	and link.target_slot.name == nodenet.exit_node_list[1]

def _softmax(output):
	exp_output = np.exp(output - np.max(output))
	return exp_output / exp_output.sum()

def _one_hot_to_int(one_hot):
	max_output = 0
	max_index = 0

	for node_index, node_output in enumerate(np.nditer(one_hot)):
		if node_output > max_output:
			max_output = node_output
			max_index = node_index

	return max_index
