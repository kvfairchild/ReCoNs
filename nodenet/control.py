from .nodenet import Nodenet

def run():
	return _step_function()

def _step_function():
	output = None

	while output is None:
		_net_function()
		output = _link_function()
		_zero_gates()

		print
	return output

# call node function for nodes that received activation
def _net_function():
	node_dict = Nodenet.Instance().node_dict

	for key in node_dict:
		node = node_dict.get(key)
		for slot in node.slot_vector:
			if slot.activation > 0:
				node.node_function(slot.activation)
				slot.activation = 0

# multiply active node gate values with link weights, sum in target slots
def _link_function():
	for link in Nodenet.Instance().links_list:
		if link.origin_gate.is_active():
			_send_activation_to_target_slot(link)
			
			# if calculation reaches exit node, return output
			if _is_exit_node(link):
				return link.target_slot.activation

# HELPER FUNCTIONS
def _zero_gates():
	for link in Nodenet.Instance().links_list:
		if link.origin_gate.activation > 0:
			link.origin_gate.activation = 0

def _send_activation_to_target_slot(link):
	activation = link.origin_gate.activation * link.weight
	link.target_slot.activation = link.target_slot.activation + activation
	print "target node:", link.target_node.name, ":", link.target_slot.activation

def _is_exit_node(link):
	return link.target_node.name == Nodenet.Instance().exit_node_list[0]\
	and link.target_slot.name == Nodenet.Instance().exit_node_list[1]