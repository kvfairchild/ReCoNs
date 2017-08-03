import unittest
from mock import MagicMock

from nodenet import config
from nodenet import control
from nodenet.node import Node
from nodenet.nodenet import Nodenet

from input_config import *

class TestControl(unittest.TestCase):

	def setUp(self):
		config.add_nodes(node_data)
		config.link_nodes(link_data)
		config.initialize_root_node(*root_node_data)
		config.set_exit_node(*exit_node_data)

	def test_run(self):
		control._step_function = MagicMock()
		control.run()

		self.assertTrue(control._step_function.called)

	def test_step_function(self):
		control._net_function = MagicMock()
		control._link_function = MagicMock()
		control._link_function.return_value = "OUTPUT"
		control._zero_gates = MagicMock()

		self.assertEqual(control._step_function(), "OUTPUT")
		self.assertTrue(control._net_function.called)
		self.assertTrue(control._link_function.called)
		self.assertTrue(control._zero_gates.called)

	def test_net_function(self):
		for node in Nodenet.Instance().node_dict.values():
			node.node_function = MagicMock()
			for slot in node.slot_vector:
				slot.activation = 0

		control._net_function()
		for node in Nodenet.Instance().node_dict.values():
			self.assertFalse(node.node_function.called)

	# def tearDown(self):
	# 	node_dict = Nodenet.Instance().node_dict

	# 	for key in node_dict.keys():
	# 		node_dict.pop(key)

if __name__ == '__main__':
	unittest.main()
