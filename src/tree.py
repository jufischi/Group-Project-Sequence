import unittest
import numpy as np


class Node:
    """
    A class used to represent a Node in a tree.

    Attributes
    ----------
    data :
        The label associated with the node
    parent : Node, optional
        The parent node of the node (default is None)
    edge_length_to_parent: float, optional
        The length of the edge from the node to its parent (default is None)
    children : list
        List of Nodes of the children of the Node

    Methods
    -------
    add_child(data, edge_length=None)
        adds a child to the node given its label and an optional edge_length
    add_child_node(child)
        adds a child node to the node
    prune_child(child)
        removes the child node from the node
    is_leaf()
        checks whether the node is a leaf
    is_root()
        checks whether the node is the root
    get_newick(with_edge_lengths=True, with_semicolon=True)
        returns a Newick string for the tree below the given node (including it)
    get_annotation()
        returns the annotation of the tree below the given node (including it)
    get_leaves()
        returns a list of all leaf nodes that are located below the node
    get_root()
        returns the root located above the given node
    copy_tree()
        returns a deep copy of the tree starting from the given node
    compute_hotspots()
        returns a dictionary containing the number of outgoing flights from each location
    get_hotspots()
        returns a String containing the locations with outgoing flights as well as their number of outgoing flights to
        other locations in a comma-separated format
    """
    def __init__(self, data, parent=None, edge_length_to_parent=None):
        """
        Parameters
        ----------
        data :
            The label associated with the node
        parent : Node, optional
            The parent node of the node (default is None)
        edge_length_to_parent: float, optional
            The length of the edge from the node to its parent (default is None)
        """
        self.data = data
        self.parent = parent
        self.edge_length_to_parent = edge_length_to_parent
        self.children = []

    def add_child(self, data, edge_length=None):
        """
        Adds a child to the node given its label and an optional edge_length.

        Parameters
        ----------
        data :
            The label associated with the node
        edge_length: float, optional
            The length of the edge from the node to its parent (default is None)
        """
        child = Node(data, self, edge_length)
        self.add_child_node(child)

    def add_child_node(self, child):
        """
        Adds a child node to the node.

        Parameters
        ----------
        child : Node
            The node that is added to the node as a child.
        """
        if child.parent is None:
            child.parent = self
        self.children.append(child)

    def prune_child(self, child):
        """
        Removes the child node from the node. Also removes the whole subtree below the child node.

        Parameters
        ----------
        child : Node
            The node that is removed from the node as a child.
        """
        self.children.remove(child)

    def is_leaf(self):
        """
        Checks whether the node is a leaf node.

        Returns
        -------
        boolean
            True if node is a leaf, False else
        """
        return len(self.children) == 0

    def is_root(self):
        """
        Checks whether the node is the root node.

        Returns
        -------
        boolean
            True if node is the root, False else
        """
        return self.parent is None

    def get_newick(self, with_edge_lengths=True, with_semicolon=True):
        """
        Returns a Newick string for the tree below the given node (including it)

        Parameters
        ----------
        with_edge_lengths : bool
            Whether the Newick string should contain edge lengths
        with_semicolon : bool
            Whether a semicolon is put at the end of the Newick string

        Returns
        -------
        String
            Newick string
        """
        result = ""
        if not self.is_leaf():
            result += "("
            for child in self.children[:-1]:
                result += child.get_newick(with_edge_lengths, with_semicolon=False)
                result += ", "
            result += self.children[-1].get_newick(with_edge_lengths, with_semicolon=False)
            result += ")"
        result += str(self.data)
        if with_edge_lengths and self.edge_length_to_parent is not None:
            result += f":{self.edge_length_to_parent}"
        if with_semicolon:
            result += ";"
        return result

    def get_annotation(self):
        """
        Returns the annotation of the tree below the given node (including it). Does not require any parameters.
        Can only be used with tree objects that have TreeLabel objects as their data.

        Returns
        -------
        String
            annotation
        """
        def get_labels(node):
            result = f"{node.data.info}\t{str(node.data)}\n"
            for child in node.children:
                result += get_labels(child)
            return result
        return "label\tlocation\n" + get_labels(self)

    def __str__(self):
        """
        Returns a formatted output String for printing the tree starting at the node.

        Returns
        -------
        String
            formatted output
        """
        return self._get_str_for_root("", True)

    def _get_str_for_root(self, prev_line, is_last):
        """
        Internal function for use in __str__(). SHOULD NOT be used by itself. Is used
        to implement the recursion necessary for drawing the tree.
        Returns a formatted output String for printing the tree starting at the node.

        Returns
        -------
        String
            formatted output
        """
        if is_last:
            result = f"{prev_line}└─ {self.data}\n"
            if not self.is_leaf():
                for child in self.children[:-1]:
                    result += child._get_str_for_root(prev_line + "   ", False)
                result += self.children[-1]._get_str_for_root(prev_line + "   ", True)
            return result
        else:
            result = f"{prev_line}├─ {self.data}\n"
            if not self.is_leaf():
                for child in self.children[:-1]:
                    result += child._get_str_for_root(prev_line + "│  ", False)
                result += self.children[-1]._get_str_for_root(prev_line + "│  ", True)
            return result

    def get_leaves(self):
        """
        Returns a list of all leaf nodes that are located below the node.

        Returns
        -------
        list
            a list of Nodes containing all leaf nodes below the given node.
        """
        if self.is_leaf():
            return [self]
        result = []
        for child in self.children:
            result.extend(child.get_leaves())
        return result

    def get_root(self):
        """
        Returns the root located above the given node.

        Returns
        -------
        Node
            the root node of the tree currently looked at
        """
        if self.is_root():
            return self
        parent = self.parent
        return parent.get_root()

    def copy_tree(self):
        """
        Returns a deep copy of the tree starting from the given node.

        Returns
        -------
        tree_copy : Node
            the root node of the copied tree
        """
        def recursion(copy, original):
            """
            This function performs the recursive step of the deepcopy function.

            Parameters
            ----------
            copy : Node
                the copied tree
            original : Node
                the original tree
            """
            child_node = Node(original.data, copy, original.edge_length_to_parent)
            copy.add_child_node(child_node)
            for child in original.children:
                recursion(child_node, child)

        # Generate root node for the copy
        tree_copy = Node(self.data, self.parent, self.edge_length_to_parent)
        for child in self.children:  # for each child of the root, do the recursion
            recursion(tree_copy, child)
        return tree_copy

    def compute_hotspots(self):
        """
        Returns a dictionary containing the locations as keys and the number of outgoing flights from each location
        as values. Resulting dictionaries contains all locations with outgoing edges (i.e. children). For counting the
        number of outgoing flights only those children are considered that have a different label. Thus, locations that
        only have outgoing edges to nodes with the same label get assigned value 0.

        Returns
        -------
        hot_spots : dict
            the number of outgoing flights from each location
        """
        hot_spots = {}

        if not self.is_leaf():
            data = str(self.data)
            if data in hot_spots.keys():
                hot_spots[data] += len([x for x in self.children if str(x.data) != data])
            else:
                hot_spots[data] = len([x for x in self.children if str(x.data) != data])

        for child in self.children:
            temp_hot_spots = child.compute_hotspots()
            hot_spots = {x: temp_hot_spots.get(x, 0) + hot_spots.get(x, 0)
                         for x in set(hot_spots).union(temp_hot_spots)}

        return hot_spots

    def get_hotspots(self):
        """
        Returns a String containing the locations with outgoing flights as well as their number of outgoing flights to
        other locations in a comma-separated format. The locations are sorted in descending order of their number of
        outgoing flights.

        Returns
        -------
        hot_spots : String
            the number of outgoing flights from each location in descending order
        """
        temp_hotspots = self.compute_hotspots()

        # sorting the dictionary by descending values:
        keys = list(temp_hotspots.keys())
        values = list(temp_hotspots.values())
        sorted_val_index = np.argsort(values)
        temp_hotspots = {keys[i]: values[i] for i in sorted_val_index[::-1]}

        # converting into String
        hot_spots = "location,no. of outgoing flights\n"
        for key, value in temp_hotspots.items():
            hot_spots += key + "," + str(value) + "\n"

        return hot_spots


class TestNode(unittest.TestCase):
    """
    A class to test the class Node.
    """
    def test_single_node_data(self):
        data = 1
        node = Node(data)
        self.assertEqual(node.data, data)

    def test_single_node_is_leaf(self):
        node = Node(1)
        self.assertEqual(node.is_leaf(), True)

    def test_single_node_is_root(self):
        node = Node(1)
        self.assertEqual(node.is_root(), True)

    def test_add_child(self):
        root = Node(1)
        root.add_child(2)
        self.assertEqual(len(root.children), 1)
        child = root.children[0]
        self.assertTrue(child.is_leaf())
        self.assertFalse(child.is_root())

    def test_add_child_node(self):
        root = Node(1)
        child = Node(2)
        root.add_child_node(child)
        self.assertEqual(len(root.children), 1)
        child = root.children[0]
        self.assertTrue(child.is_leaf())
        self.assertFalse(child.is_root())

    def test_add_child_with_edge_length(self):
        edge_length = 2.45
        root = Node(1)
        root.add_child(2, edge_length)
        child = root.children[0]
        self.assertEqual(child.edge_length_to_parent, edge_length)

    def test_get_leaves(self):
        root = Node(1)
        root.add_child(2)
        root.add_child(3)
        internal_node = Node(4)
        internal_node.add_child(5)
        internal_node.add_child(6)
        root.add_child_node(internal_node)
        leaves = map(lambda x: x.data, root.get_leaves())
        self.assertIn(2, leaves)
        self.assertIn(3, leaves)
        self.assertIn(5, leaves)
        self.assertIn(6, leaves)

    def test_get_root(self):
        root = Node(1)
        internal_node = Node(2)
        leaf_node = Node(3)
        internal_node.add_child_node(leaf_node)
        root.add_child_node(internal_node)
        determined_root = leaf_node.get_root()
        self.assertEqual(root, determined_root)

    def test_prune_child(self):
        root = Node(1)
        root.add_child(2)
        root.add_child(3)
        internal_node = Node(4)
        internal_node.add_child(5)
        internal_node.add_child(6)
        root.add_child_node(internal_node)
        root.prune_child(internal_node)
        leaves = map(lambda x: x.data, root.get_leaves())
        self.assertIn(2, leaves)
        self.assertIn(3, leaves)
        self.assertNotIn(5, leaves)
        self.assertNotIn(6, leaves)

    def test_copy_tree(self):
        root = Node(1)
        root.add_child(2)
        root.add_child(3)
        internal_node = Node(4)
        internal_node.add_child(5)
        internal_node.add_child(6)
        root.add_child_node(internal_node)
        root_copy = root.copy_tree()
        self.assertEqual(internal_node.data, root_copy.children[2].data)
        root_copy.children[2].data = 7
        self.assertNotEqual(internal_node.data, root_copy.children[2].data)

    def test_compute_hotspots(self):
        root = Node(1)
        root.add_child(2)
        root.add_child(3)
        internal_node = Node(4)
        internal_node.add_child(5)
        internal_node.add_child(6)
        root.add_child_node(internal_node)
        internal_node.add_child(4)
        internal_node.children[2].add_child(7)
        root.children[1].add_child(4)
        root.children[1].children[0].add_child(8)
        hot_spots = root.compute_hotspots()
        self.assertEqual(hot_spots['1'], 3)
        self.assertEqual(hot_spots['4'], 4)
        self.assertNotIn('2', hot_spots)


class TreeLabel:
    """
    A class to store the information about a node in the tree

    Attributes
    ----------
    label : String
        information about the location (airport or country)
    info : String
        additional information about the node (e.g. sequence ID)
    array : np.array
        stores cost at each node and node label for computation of Sankoff
    label_index: int
        index of the label in the distance matrix header
    """
    def __init__(self, label, info, array, label_index):
        self.label = label
        self.info = info
        self.array = array
        self.label_index = label_index

    def __str__(self):
        return str(self.label)


if __name__ == '__main__':
    unittest.main()
