import unittest

from nodenet import config
from nodenet import control
from nodenet.nodenet import Nodenet

from sample_input import *

class TestControl(unittest.TestCase):

	def setUp(self):
		config.add_nodes(node_data)
		config.link_nodes(link_data)
		config.initialize_root_node(*root_node_data)
		config.set_exit_node(*exit_node_data)

		control.run()

if __name__ == '__main__':
	unittest.main()