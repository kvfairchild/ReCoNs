from __future__ import division
from itertools import chain

from request_confirmation import request_confirmation
from stack import Stack

def run(recon, symbol_array):
    ops = _prep_data(symbol_array)

    _input_symbols(recon, ops)
    _activate_root_node(recon, .6)
    output = _step_function(recon)

    print "Function value: ", output, "\n"

# insert identified symbols into last layer nodes
def _input_symbols(recon, ops):
    global last_layer
    last_layer = recon.layers[len(recon.layers)-1]

    for node_index, node in enumerate(last_layer):
        # leave last node empty for function value
        if node_index != len(last_layer)-1:
            node.value = ops[node_index]

# initialize ReCoN via root node "sub" activation
def _activate_root_node(recon, activation):
    global root_node
    root_node = recon.layers[0][0]

    slot = root_node.get_slot("sub")
    slot.activation = activation

    # move activation from slot into node
    _net_function(recon)

def _step_function(recon):
    stack = Stack()
    eval_node = last_layer[len(last_layer)-1]

    while 0 < root_node.activation < 1:

        for layer in recon.layers:

            request_confirmation(recon)
            _net_function(recon)
            _link_function(recon)

            if layer == last_layer:
                for node in layer:
                    node.push_to_stack(stack)
                    node.pull_from_stack(stack)

            print "\n"
            for node in layer:
                print node.name, node.activation

        _zero_gates(recon)

        if root_node.activation >= 1:
            print "\nCONFIRMED"
            return eval_node.value
        elif root_node.activation <= 0:
            print "\nFAILED"
            return
        else:
            root_node.activation = .6

# call node function for nodes that received activation
def _net_function(recon):
    node_dict = recon.node_dict

    for node in node_dict.values():
        for slot in node.slot_vector:
            if slot.activation != 0:
                node.activation += slot.activation
                node.node_function(slot.activation)
                slot.activation = 0

# multiply node gate values with link weights, sum in target slots
def _link_function(recon):
    for layer in recon.links_list:
        for link in layer:
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
