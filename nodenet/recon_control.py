from __future__ import division
from itertools import chain

from request_confirmation import request_confirmation
from stack import Stack

def run(recon, symbol_array):
    ops = _prep_data(symbol_array)

    _input_symbols(recon, ops)
    _activate_root_node(recon, .4)
    _step_function(recon)

def _input_symbols(recon, ops):
    global LAST_LAYER
    LAST_LAYER = recon.layers[len(recon.layers)-1]

    for node_index, node in enumerate(LAST_LAYER):
        if node_index != len(LAST_LAYER)-1:
            node.value = ops[node_index]

# initialize ReCoN via root node "sub" activation
def _activate_root_node(recon, activation):

    for node in recon.layers[0]:

        slot = node.get_slot("sub")
        slot.activation = activation

def _step_function(recon):
    stack = Stack()
    eval_node = LAST_LAYER[len(LAST_LAYER)-1]

    while any(node.activation < 1 for node in recon.layers[0]):

        for layer in recon.layers:

            _net_function(recon)
            _link_function(recon)

            request_confirmation(recon)

            if layer == LAST_LAYER:
                for node in layer:
                    node.push_to_stack(stack)
                    node.pull_from_stack(stack)

            for node in recon.node_dict.values():
                if node.activation > 0:
                    print node.name, node.activation
            
            function_value = eval_node.value

            # for node in LAST_LAYER:
            #     print node.name, node.activation, node.value

            # print "function_value: ", function_value

            _zero_nodes(recon)
            _zero_gates(recon)

        print "*********************************"


# call node function for nodes that received activation
def _net_function(recon):
    node_dict = recon.node_dict

    for node in node_dict.values():
        for slot in node.slot_vector:
            if slot.activation != 0:
                node.activation += slot.activation
                node.node_function(slot.activation)
                slot.activation = 0

# multiply active node gate values with link weights, sum in target slots
def _link_function(recon):
    for layer in recon.links_list:
        for link in layer:
            if link.origin_gate.is_active():
                _send_activation_to_target_slot(link)


# HELPER FUNCTIONS

def _prep_data(symbol_array):
    ops = []
    
    # split symbol array into suboperations
    ops.append(symbol_array[0:3])
    for i in range(3,len(symbol_array),2):
        ops.append(symbol_array[i:i+2])
    
    # reverse order of symbols (e.g. 1,+,2 --> 1,2,+)
    for op in ops:
        op[-2:] = reversed(op[-2:])

    # join sublists of now reversed operations into one list
    ops = list(chain.from_iterable(ops))

    return ops

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
