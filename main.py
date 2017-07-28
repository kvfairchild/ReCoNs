#!/usr/bin/env python

from nodenet import config
from nodenet import control

from test.input_config import *

if __name__ == "__main__":

	config.add_nodes(node_data)
	config.link_nodes(link_data)
	config.initialize_root_node(*root_node_data)
	config.set_exit_node(*exit_node_data)

	control.run()