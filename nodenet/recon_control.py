from __future__ import division

def run(recon, symbol_array):

    i = 0

    while i < len(symbol_array):
        _activate_recon(recon, .8)

        _step_function(recon)

        i += 1

# initialize ReCoN via root node "sub" activation
            
def _activate_recon(recon, activation):

    for node in recon.layers[0]:

        slot = node.get_slot("sub")
        slot.activation = activation

def _step_function(recon):

    while any(slot.activation > 0 for node in recon.node_dict.values() for slot in node.slot_vector):

        for layer in recon.layers:

            _net_function(recon)
            _link_function(recon)

            for node in recon.node_dict.values():
                if node.activation > 0:
                    print node.name, node.activation

            _propagate_activation(recon)

            _zero_nodes(recon)
            _zero_gates(recon)

        print "*********************************"
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

def _propagate_activation(recon):

    """ 

    ReCoN nodes are state machines that use the node activation for determining their behavior.

    They form hierarchical scripts that are started via sub-activating their top-node. If the sur-activation
    is turned off, the script stops executing.
    
    At the bottom, the scripts must connect to activation sources (that yield positive sur activation), otherwise
    they will fail.
    
    The links have the following semantics:
    
    - sub determines sub-actions. Inactive sub-actions will turn "ready" if their parent action turns
    "requesting", by sending activation via sub.
    - por determines successors. If an action is neither inactive nor confirmed, it will inhibit its successors
    from requesting. Successors must wait for their predecessors to stop sending por-activation. The first
    action in a por-chain receives no such inhibition, it may turn from "ready" to "requesting". After
    an action has become "requesting", it turns "pending" and continues to request its sub-actions.
    All other "ready" actions will switch to "waiting" until their predecessors stop inhibiting them.
    - ret determines predecessors. Successors inhibit their predecessors from telling their parents when they
    confirm. (Once an action without sucessor confirms, we are done.)
    - sur has two functions. A high level of sur activation confirms the parent action. A low level of sur
    tells the parent action that at least one of its sub-actions has not given up yet. If no more sur
    activation is received by a pending parent action, it will fail.
    The distinction between "ready" and "waiting", and "requesting and "pending" is necessary to bridge the
    time until neighboring nodes have had time to make themselves heard.

    Currently, the node states correspond to the following activation levels:
    < 0     failed (will stick until requesting ends)
    < 0.01  inactive (will change to prepared when requested)
    < 0.3   preparing (inhibits neighbors  and changes to suppressed)
    < 0.5   suppressed (inhibits neighbors and goes to requesting when no longer inhibited)
    < 0.7   requesting (starts requesting and changes to pending)
    < 1     pending (keeps requesting, will either change to confirmed or failed)
    >=1     confirmed (will stick until requesting ends)

    """

    node_dict = recon.node_dict

    for node in node_dict.values():

        if node.get_slot("sub").activation < 0.01:  # node is not requested and is turned off
            node.activation = 0.0
            node.get_gate("por").gate_function(0.0)
            node.get_gate("ret").gate_function(0.0)
            node.get_gate("sub").gate_function(0.0)
            node.get_gate("sur").gate_function(0.0)
            return

        node.activation = (
        node.activation if node.activation < -0.01 else  # failed -> failed
        0.2 if node.activation < 0.01 else  # (already tested that sub is positive): inactive -> preparing
        0.4 if node.activation < 0.5 and node.get_slot("por").activation < 0 else  # preparing -> supressed
        0.6 if node.activation < 0.5 else  # preparing/supressed -> requesting
        0.8 if node.activation < 0.7 else  # requesting -> pending
        1.0 if node.get_slot("sur").activation >= 1 else  # pending -> confirmed
        -1. if node.get_slot("sur").activation <= 0 else  # pending -> failed
        node.activation
        )

        # always inhibit successor, except when confirmed
        node.get_gate("por").gate_function(-1.0 if node.activation < 1 else 1.0)
        # inhibit confirmation of predecessor, and tell it to stop once successor is requested
        node.get_gate("ret").gate_function(-1.0 if 0.1 < node.activation < 1 else 1.0)
        # request children when becoming requesting
        node.get_gate("sub").gate_function(1.0 if 0.5 < node.activation else 0)
        # keep parent from failing while pending or processing, confirm parent when confirmed
        node.get_gate("sur").gate_function(
        0 if node.activation < 0.01 or node.get_slot("ret").activation > 0 else
        0.01 if node.activation < 1 else
        0.01 if node.get_slot("ret").activation < 0 else
        1)

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
