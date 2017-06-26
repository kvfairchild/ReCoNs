from .nodenet import Nodenet

def run():
	return _step_function()

def _step_function():
	output = None
	while output is None:
		_net_function()
		output = _link_function()

	return output

# multiplies active node gate values with link weights, sums them in target slots
def _link_function():
	for link in Nodenet.Instance().links_list:
		if link.origin_gate.is_active():
			activation = link.origin_gate.activation * link.weight
			link.target_slot.activation = link.target_slot.activation + activation
			print link.target_slot.activation
			
			if link.target_node.name == Nodenet.Instance().tail_list[0]\
			and link.target_slot.name == Nodenet.Instance().tail_list[1]:
				return link.target_slot.activation

def _net_function():
	node_dict = Nodenet.Instance().node_dict

	for key in node_dict:
		node = node_dict.get(key)
		for slot in node.slot_vector:
			if slot.activation > 0:
				node.node_function(slot.activation)
				slot.activation = 0
