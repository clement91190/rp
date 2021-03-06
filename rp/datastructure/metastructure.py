# -*-coding:Utf-8 -*
import math
import numpy as np
import pickle
nb = 0


class Node:
    """ a node is the elementary piece of the structure
    a Node has a father ( unless it is the head) and children
    """
    def __init__(self, father):
        self.edges = [father]
        self.ind = 0

    def set_father(self, father):
        self.edges[0] = father

    def set_edge(self, node, ind=1):
        self.edges[ind] = node

    def get_linked_link(self):
        l = []
        for edge in self.edges[1:]:
            if edge is not None:
                if edge.gen_type() == "shape":
                    l += edge.get_linked_link()
                elif edge.gen_type() == "link":
                    l.append(edge.ind)
        return l


class EmptyNode(Node):
    """ Empty node """
    def type(self):
        return "empty"

    def gen_type(self):
        return "empty"


class Block(Node):
    """ a block is a cubical shaped node with 6 face (so 6
    potential edges)"""
    def __init__(self, father):
        Node.__init__(self, father)
        for i in range(1, 6):
            self.edges.append(EmptyNode(self))

    def type(self):
        return "block"

    def gen_type(self):
        return "shape"


class Joint(Node):
    """ a joint is a link with 1 degree of freedom
    (think servomotor)
    orientation is 0 or 1 => 2 directions are possible
    """
    def __init__(self, father, orientation=1):
        Node.__init__(self, father)
        self.edges.append(EmptyNode(self))
        self.angle = 0
        self.orientation = orientation
        global nb
        nb = nb + 1
        print "########### nb {}".format(nb)
        self.phi = nb * math.pi * 0.5

    def type(self):
        return "joint"

    def gen_type(self):
        return "link"


class Vertebra(Node):
    """ a Vertebra is a node with 2 degrees of freedom, that
    can only be linked to 2 other vertebra or be the end of the
    vertebral column """
    def __init__(self, father):
        Node.__init__(self, father)
        self.edges.append(EmptyNode(self))
        self.angle1 = 0
        self.angle2 = 0
        global nb
        nb = nb + 1
        print "########### nb {}".format(nb)
        self.phi = nb * math.pi * 0.5

    def type(self):
        return "vertebra"

    def gen_type(self):
        return "link"


class Head(Node):
    """ Head of the structure,
    by default a head has no father ( but it
    is possible to add one for circular structure for instance
    )"""
    def __init__(self):
        Node.__init__(self, None)
        for i in range(1, 6):
            self.edges.append(EmptyNode(self))

    def type(self):
        return "head"

    def gen_type(self):
        return "shape"


class MetaStructure:
    """ definition of the structure of the robots
    and tools to explore and create nodes"""
    def __init__(self):
        self.head = Head()
        self.current = self.head  # indicate the current Node
        self.selector = 1  # indicate the edge selected 0 is always the father
        self.all_nodes = [self.head]
        self.dof_nodes = []

    def follow_edge(self, ind=1):
        self.current = self.current.edges[self.selector]
        self.selector = ind

    def next_edge(self):
        self.selector += 1

    def previous_edge(self):
        self.selector -= 1

    def set_current(self, ind=0):
        self.current = self.all_nodes[ind]

    def set_selector(self, ind=1):
        self.selector = ind

    def follow_father(self, ind=1):
        self.selector = 0
        self.follow_edge(ind)

    def add_joint(self, orient=1):
        node = Joint(self.current, orient)
        self.current.edges[self.selector] = node
        self.all_nodes.append(node)
        self.dof_nodes.append(node)
        node.ind = len(self.dof_nodes) - 1

    def add_vertebra(self):
        node = Vertebra(self.current)
        self.current.edges[self.selector] = node
        self.all_nodes.append(node)
        self.dof_nodes.append(node)
        node.ind = len(self.dof_nodes) - 1

    def add_block(self):
        node = Block(self.current)
        self.current.edges[self.selector] = node
        self.all_nodes.append(node)

    def size(self):
        """ return the number of nodes """
        return len(self.dof_nodes)

    def compute_and_get_connectivity_matrix(self):
        m = np.matrix(np.eye(self.size()))
        for i, node1 in enumerate(self.dof_nodes):
            #print node1.get_linked_link()
            for j in node1.get_linked_link():
                m[i, j] = 1
                m[j, i] = 1
        #print m
        return m

    def get_angle_dict(self):
        return {node: 0 for node in self.dof_nodes}

    def save_structure(self, name='creature.txt'):
        """ save the structure creating a file with name name"""
        with open(name, 'r') as fich:
            pickle.dump(fich, self)


def load_structure(name="creature.txt"):
    """ function to load a structure from a file in the
    structure folder"""
    with open(name) as fich:
        return pickle.load(fich)


