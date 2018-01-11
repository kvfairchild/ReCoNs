#!/usr/bin/env python

from __future__ import division

from request_confirmation import request_confirmation

def run(recon, symbol_array):

    _input_symbols(recon, symbol_array)
    _activate_root_node(recon, .8)
    _step_function(recon)

def _input_symbols(recon, symbol_array):

    for node_index, node in enumerate(recon.layers[len(recon.layers)-1]):

        print node.name, symbol_array[node_index]

        slot = node.get_slot("sur")
        slot.activation = symbol_array[node_index]

# initialize ReCoN via root node "sub" activation
def _activate_root_node(recon, activation):

    for node in recon.layers[0]:

        slot = node.get_slot("sub")
        slot.activation = activation

def _step_function(recon):

    while any(slot.activation > 0 for node in recon.node_dict.values() for slot in node.slot_vector):

        for layer in recon.layers:

            _net_function(recon)
            _link_function(recon)

            request_confirmation(recon)

            for node in recon.node_dict.values():
                if node.activation > 0:
                    print node.name, node.activation

            _zero_nodes(recon)
            _zero_gates(recon)

        print "*********************************"


# call node function for nodes that received activation
def _net_function(nodenet):
    node_dict = nodenet.node_dict

    for node in node_dict.values():
        for slot in node.slot_vector:
            if slot.activation != 0:
                node.activation += slot.activation
                node.node_function(slot.activation)
                slot.activation = 0

# multiply active node gate values with link weights, sum in target slots
def _link_function(nodenet):
    for layer in nodenet.links_list:
        for link in layer:
            if link.origin_gate.is_active():
                _send_activation_to_target_slot(link)


# HELPER FUNCTIONS

def _send_activation_to_target_slot(link):
    activation = link.origin_gate.activation * link.weight
    link.target_slot.activation += activation

def _zero_gates(recon):
    for layer in recon.links_list:
        for link in layer:
            link.origin_gate.activation = 0

def _zero_nodes(recon):
    for layer in recon.layers:
        for node in layer:
            node.activation = 0
