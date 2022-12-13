import unittest


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
    is_leaf()
        checks whether the node is a leaf
    is_root()
        checks whether the node is the root
    get_leaves()
        returns a list of all leaf nodes that are located below the node
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
        self.children.append(child)

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


if __name__ == '__main__':
    unittest.main()
