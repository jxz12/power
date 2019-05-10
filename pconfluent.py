import power as cpp
import numpy as np

class routing_node:
    def __init__(self, idx):
        self.idx = idx
        self.incoming = []
        self.outgoing = []
        self.power = []

    def add_child(self, child):
        self.outgoing.append(child)
        child.incoming.append(self)

    def add_poweredge(self, neighbour):
        self.power.append(neighbour)
        neighbour.power.append(self)
        
def init_routing_nodes(Ir, Jr, Ip, Jp):
    nodes = {}
    # do routing
    for ij in range(len(Ir)):
        i = Ir[ij]
        j = Jr[ij]
        if i not in nodes.keys():
            nodes[i] = routing_node(i)
        if j not in nodes.keys():
            nodes[j] = routing_node(j)

        nodes[i].add_child(nodes[j])

    # add power edges
    for ij in range(len(Ip)):
        i = Ip[ij]
        j = Jp[ij]
        nodes[i].add_poweredge(nodes[j])

    # # split crossing-artifact nodes
    # for node in routing_nodes:

    return nodes


# post-order traversal to init paths to one end
def init_paths_from_leaves(node, stack, paths):
    stack.append(node.idx)
    if len(node.outgoing) == 0:
        # if leaf, create path
        paths.append([i for i in reversed(stack)])
    else:
        for child in node.outgoing:
            init_paths_from_leaves(child, stack, paths)
    stack.pop()

# pre-order traversal to finish paths from other end
def finish_paths_to_leaves(node, stack, paths_from, all_paths):
    stack.append(node.idx)
    if len(node.outgoing) == 0:
        # if leaf, finish path
        path_to = [i for i in stack]
        for path_from in paths_from:
            all_paths.append(path_from + path_to)
    else:
        for child in node.outgoing:
            finish_paths_to_leaves(child, stack, paths_from, all_paths)
    stack.pop()


# I = [0,0,0, 1,1,1, 2,2,2]
# J = [3,4,5, 3,4,5, 3,4,5]
# Ir, Jr, Ip, Jp = cpp.routing(6, I, J)

Ir = [6,6,6, 7,7,7]
Jr = [0,1,2, 3,4,5]
Ip = [6]
Jp = [7]

R = init_routing_nodes(Ir, Jr, Ip, Jp)

all_paths = []
for ij in range(len(Ip)):
    i = Ip[ij]
    j = Jp[ij]
    paths_from = []
    init_paths_from_leaves(R[i], [], paths_from)
    finish_paths_to_leaves(R[j], [], paths_from, all_paths)

print("paths:")
print(all_paths)

