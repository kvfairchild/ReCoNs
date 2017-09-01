from .nodenet import Nodenet

def run(nodenet):
	return _step_function(nodenet)

def _step_function(nodenet):
	output = None

	for layer in nodenet.layers:
		_net_function(nodenet)
		output = _link_function(nodenet)
		_zero_gates(nodenet)


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
	print "target node:", link.target_node.name, ":", link.target_slot.activation

def _is_exit_node(nodenet, link):
	return link.target_node.name == nodenet.exit_node_list[0]\
	and link.target_slot.name == nodenet.exit_node_list[1]
