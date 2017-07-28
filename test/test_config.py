import unittest

from nodenet import config
from nodenet.node import Node
from nodenet.nodenet import Nodenet

from sample_input import *

class TestConfig(unittest.TestCase):
	def setUp(self):
		config.add_nodes(node_data)

	def test_add_nodes(self):
		for new_node in node_data:
			node_name = new_node[0]
			node = Nodenet.Instance().node_dict.get(node_name)
			self.assertEquals(node.name, node_name)

	def test_remove_nodes(self):
		initial_length = len(Nodenet.Instance().node_dict)
		node_name = node_data[0][0]
		config.remove_nodes([node_name])
		self.assertNotEqual(initial_length, len(Nodenet.Instance().node_dict))

if __name__ == '__main__':
    unittest.main()
