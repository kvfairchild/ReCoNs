import unittest
from mock import patch
from mock import MagicMock

from nodenet import config
from nodenet import control
from nodenet.node import Node
from nodenet.nodenet import Nodenet

from input_config import *

class TestControl(unittest.TestCase):

	def setUp(self):
		self.nodenet = Nodenet()
		config.add_nodes(self.nodenet, node_data)
		config.link_nodes(self.nodenet, link_data)
		config.initialize_root_node(self.nodenet, *root_node_data)
		config.set_exit_node(self.nodenet, *exit_node_data)

	@patch("nodenet.control._step_function")
	def test_run(self, _step_function):
		control.run(self.nodenet)

		self.assertTrue(_step_function.called)

	def test_step_function(self):
		control._net_function = MagicMock()
		control._link_function = MagicMock()
		control._link_function.return_value = "OUTPUT"
		control._zero_gates = MagicMock()

		self.assertEqual(control._step_function(self.nodenet), "OUTPUT")
		self.assertTrue(control._net_function.called)
		self.assertTrue(control._link_function.called)
		self.assertTrue(control._zero_gates.called)

	def test_net_function(self):
		for node in self.nodenet.node_dict.values():
			node.node_function = MagicMock()
			for slot in node.slot_vector:
				slot.activation = 0

		control._net_function(self.nodenet)
		for node in self.nodenet.node_dict.values():
			self.assertFalse(node.node_function.called)

if __name__ == '__main__':
	unittest.main()
