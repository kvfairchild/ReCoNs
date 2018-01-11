from __future__ import division

from request_confirmation import request_confirmation

def run(recon, symbol_array):

    subops = _prep_subops(symbol_array)
    _input_symbols(recon, subops)
    _activate_root_node(recon, .8)
    _step_function(recon)

def _input_symbols(recon, subops):
    last_layer = recon.layers[len(recon.layers)-1]

    for node_index, node in enumerate(last_layer[0:3]):
        node.value = subops[0][node_index]
        
    i = 1 # subops index
    j = 0 # symbols index

    for node_index, node in enumerate(last_layer[3:len(last_layer)]):
        if node_index % 3 == 0: # leave 0-indexed digit value empty for result of preceding operation
            j += 1
        elif node_index == j:
            node.value = subops[i][0]
        elif node_index == j+1:
            node.value = subops[i][1]
            i += 1
            j += 2

        # slot = node.get_slot("sur")
        # slot.activation = symbol_array[node_index]

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

def _prep_subops(symbol_array):
    ops = []
    
    # split symbol array into suboperations
    ops.append(symbol_array[0:3])
    for i in range(3,len(symbol_array),2):
        ops.append(symbol_array[i:i+2])
    
    # reverse order of symbols (e.g. 1,+,2 --> 1,2,+)
    for op in ops:
        op[-2:] = reversed(op[-2:])

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
