import unittest

class Node:
    def __init__(self, data, parent = None, edge_length_to_parent = None):
        self.data = data
        self.parent = parent
        self.edge_length_to_parent = edge_length_to_parent
        self.children = []

    def add_child(self, data, edge_length = None):
        child = Node(data, self, edge_length)
        self.add_child_node(child)

    def add_child_node(self, child):
        self.children.append(child)

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent == None

    def __str__(self):
        result = f"{self.data}:{self.edge_length_to_parent}\n[\n"
        for child in self.children:
            result += str(child)
        return result + "]\n"

    def get_leaves(self):
        if self.is_leaf():
            return [self]
        result = []
        for child in self.children:
            result.extend(child.get_leaves())
        return result


class TestNode(unittest.TestCase):
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
