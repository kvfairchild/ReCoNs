import unittest

from nodenet import config
from nodenet.link import Link
from nodenet.node import Node
from nodenet.nodenet import Nodenet

from input_config import *

class TestConfig(unittest.TestCase):

	def setUp(self):
		self.nodenet = Nodenet()
		config.add_nodes(self.nodenet, node_data)
		config.link_nodes(self.nodenet, link_data)

	def test_add_nodes(self):
		for new_node in node_data:
			node_name = new_node[0]
			node = self.nodenet.node_dict.get(node_name)
			self.assertEquals(node.name, node_name)

	def test_remove_nodes(self):
		initial_length = len(self.nodenet.node_dict)
		node_name = node_data[0][0]
		config.remove_nodes(self.nodenet, [node_name])
		self.assertNotEqual(initial_length, len(self.nodenet.node_dict))

	def test_link_creation(self):
		for new_link in link_data:
			origin_node_name = new_link.get("origin")[0]
			target_node_name = new_link.get("target")[0]
		for link in self.nodenet.links_list:
		 	origin_node = link.origin_node.name
		 	target_node = link.target_node.name
		self.assertEquals(origin_node, origin_node_name)
		self.assertEquals(target_node, target_node_name)

	def test_nodenet_initialization(self):
		config.initialize_root_node(self.nodenet, *root_node_data)

		for node in self.nodenet.node_dict.values():
			for slot in node.slot_vector:
				if slot.activation > 0:
					activation = slot.activation 
		self.assertEquals(root_node_data[0], activation)

if __name__ == '__main__':
    unittest.main()
