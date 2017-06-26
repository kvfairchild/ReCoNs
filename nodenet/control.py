# multiplies active node gate values with link weights, sums them in target slots
def link_function(self):
	for link in self.link_list:
		if link.origin_gate.is_active():
			current_value = link.origin_gate.current_value * link.weight
			link.target_slot.current_value = link.target_slot.current_value + current_value

