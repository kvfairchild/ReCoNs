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

	@patch("nodenet.control._zero_gates")
	def test_step_function(self, _zero_gates):
		control._net_function = MagicMock()
		control._link_function = MagicMock()
		control._link_function.return_value = "OUTPUT"

		self.assertEqual(control._step_function(self.nodenet), "OUTPUT")
		self.assertTrue(control._net_function.called)
		self.assertTrue(control._link_function.called)
		self.assertTrue(_zero_gates.called)

	def test_net_function(self):
		# set slot activation to 0
		for node in self.nodenet.node_dict.values():
			node.node_function = MagicMock()
			for slot in node.slot_vector:
				slot.activation = 0
		# ensure node function not called for 0 activation
		control._net_function(self.nodenet)
		for node in self.nodenet.node_dict.values():
			self.assertFalse(node.node_function.called)
		# set slot activation to 1
		for node in self.nodenet.node_dict.values():
			node.node_function = MagicMock()
			for slot in node.slot_vector:
				slot.activation = 1
		# ensure node function called for >0 activation
		control._net_function(self.nodenet)
		for node in self.nodenet.node_dict.values():
			self.assertTrue(node.node_function.called)

	@patch("nodenet.control._send_activation_to_target_slot")
	def test_link_function(self, _send_activation_to_target_slot):
		# ensure activation not sent to target slot when origin gate is not active
		for link in self.nodenet.links_list:
			link.origin_gate.is_active = MagicMock()
			link.origin_gate.is_active.return_value = False
		control._link_function(self.nodenet)
		for link in self.nodenet.links_list:
			self.assertFalse(_send_activation_to_target_slot.called)
		# ensure activation sent to target slot when origin gate is active
		for link in self.nodenet.links_list:
			link.origin_gate.is_active = MagicMock()
			link.origin_gate.is_active.return_value = True
		control._link_function(self.nodenet)
		for link in self.nodenet.links_list:
			self.assertTrue(_send_activation_to_target_slot.called)

	@patch("nodenet.control._send_activation_to_target_slot")
	def test_link_function_exit(self, _send_activation_to_target_slot):
		for link in self.nodenet.links_list:
			link.origin_gate.is_active = MagicMock()
			link.origin_gate.is_active.return_value = True
			if link.target_node == self.nodenet.node_dict.get(exit_node_data[0]):
				link.target_slot.activation = "ACTIVATION"

		self.assertEqual(control._link_function(self.nodenet), "ACTIVATION")

	def test_zero_gates(self):
		for link in self.nodenet.links_list:
			link.origin_gate.activation = 1
		
		control._zero_gates(self.nodenet)
		for link in self.nodenet.links_list:
			self.assertEqual(link.origin_gate.activation, 0)

	def test_send_activation_to_target_slot(self):
		link = MagicMock()
		link.origin_gate = MagicMock()
		link.origin_gate.activation = 1
		link.target_slot = MagicMock()
		link.target_slot.activation = 1
		link.weight = 2

		control._send_activation_to_target_slot(link)

		self.assertEqual(link.target_slot.activation, 3)

	def test_is_exit_node(self):
		without_exit_node_links = []
		with_exit_node_links = []
		for link in self.nodenet.links_list:
			if link.target_node != self.nodenet.node_dict.get(exit_node_data[0]):
				without_exit_node_links.append(link)
			else:
				with_exit_node_links.append(link)

		for link in without_exit_node_links:
			self.assertFalse(control._is_exit_node(self.nodenet, link))
		for link in with_exit_node_links:
			self.assertTrue(control._is_exit_node(self.nodenet, link))

if __name__ == '__main__':
	unittest.main()
