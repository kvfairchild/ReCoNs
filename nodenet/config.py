# from .link import Link
# from .node_factory import node_factory


# # multiplies active node gate values with link weights, sums them in target slots
# def link_function(self):
# 	for link in self.link_list:
# 		if link.origin_gate.is_active():
# 			current_value = link.origin_gate.current_value * link.weight
# 			link.target_slot.current_value = link.target_slot.current_value + current_value

# def build_nodenet(self):
#     for layer in range(0, self.num_layers):
#     	layer = __build_layer()
#     	self.node_net.append(layer)
#     __link_nodenet(node_net)

# def __build_layer(self):
#     layer = []
#     for node in range(0, self.num_nodes):
#     	node = self.__node_factory()
#         layer.append(node)
#     return layer

# def __link_nodenet(self):
# 	# iterate through n-1 layers for origin nodes
# 	for layer_index in range(0, self.num_layers-1):
# 		for node_index in range(0, len(self.node_net[layer_index])):
# 			self.__create_link(self.node_net[layer_index][node_index], self.node_net[layer_index+1])

# def __create_link(self, origin_node, target_layer):
# 	for target_node in target_layer:
# 		for target_slot in target_node.slot_vector:
# 			self.link_list.append(self.__link_factory(origin_node, origin_node.gate_vector[0], target_node, target_slot))

# def __remove_node(self, name):
# 	self.node_dict.pop(name, None) 

# def __link_factory(self, origin_node, origin_gate, target_node, target_slot):
# 	link = Link(origin_node, origin_gate, target_node, target_slot)
# 	return link
