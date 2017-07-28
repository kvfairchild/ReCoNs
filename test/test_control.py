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

if __name__ == '__main__':
	unittest.main()