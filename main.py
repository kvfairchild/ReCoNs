#!/usr/bin/env python

from nodenet import config
from nodenet import control
from nodenet.nodenet import Nodenet

from test.input_config import *

def build_nodenet(nodenet):
	config.add_nodes(nodenet, node_data)
	config.link_nodes(nodenet, link_data)
	config.initialize_root_node(nodenet, *root_node_data)
	config.set_exit_node(nodenet, *exit_node_data)

	control.run(nodenet)

if __name__ == "__main__":
	build_nodenet(Nodenet())
