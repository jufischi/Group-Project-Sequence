from newick_parser import NewickParser
from distance_matrix import DistanceMatrix
import unittest
import numpy as np


class Sankoff:
    def __init__(self, newick_string, distance_matrix, mapping, delimiter=','):
        parser = NewickParser(newick_string)
        parser.parse()
        self.tree = parser.root

        self.distance_matrix = DistanceMatrix(distance_matrix, delimiter)
        self.mapping = mapping

        self.set_tree_labels(self.tree)

    def do_sankoff(self):
        self.forward_pass(self.tree)
        self.backward_pass(self.tree)

    def set_tree_labels(self, node):
        for child in node.children:
            self.set_tree_labels(child)
        if node.is_leaf():
            label = self.mapping[node.data]
            dictionary = dict([(x, 0) if x == label else (x, float('inf')) for x in self.distance_matrix.header])
            node.data = TreeLabel(label, node.data, dictionary)
        else:
            node.data = TreeLabel(None, node.data, {})

    def forward_pass(self, node):
        list_of_dict = []
        for child in node.children:
            list_of_dict.append(self.forward_pass(child))
        if not node.is_leaf():
            for label in self.distance_matrix.header:
                cost = 0
                for child in list_of_dict:
                    cost += min([(value + self.distance_matrix.get_distance(label, key))
                                 for key, value in child.items()])
                node.data.dictionary[label] = cost
        return node.data.dictionary

    def backward_pass(self, node):
        node.data.label, _ = self.get_minimal_cost(node)
        for child in node.children:
            self.backward_pass(child)

    def get_minimal_cost(self, node):
        if node.is_root():
            min_cost = min(node.data.dictionary.values())
            for key, value in node.data.dictionary.items():
                if value == min_cost:
                    return key, min_cost
        else:
            min_cost = float('inf')
            min_key = ""
            for key, value in node.data.dictionary.items():
                cost = value + self.distance_matrix.get_distance(node.parent.data.label, key)
                if cost < min_cost:
                    min_cost = cost
                    min_key = key
            return min_key, min_cost


class TreeLabel:
    def __init__(self, label, info, dictionary):
        self.label = label
        self.info = info
        self.dictionary = dictionary


class TestSankoff(unittest.TestCase):
    def setUp(self):
        self.newick = "(((A,C),G),(C,G));"
        self.distance_matrix = [["A", "C", "G", "T"],
                                np.array([[0, 2, 1, 2], [2, 0, 2, 1], [1, 2, 0, 2], [2, 1, 2, 0]])]
        self.mapping = {"A": "A", "C": "C", "G": "G", "T": "T"}

    def test_forward_pass(self):
        sankoff = Sankoff(self.newick, self.distance_matrix, self.mapping)
        sankoff.forward_pass(sankoff.tree)
        self.assertEqual(round(sankoff.tree.data.dictionary["A"], 0), 6)
        self.assertEqual(round(sankoff.tree.data.dictionary["C"], 0), 6)
        self.assertEqual(round(sankoff.tree.data.dictionary["G"], 0), 5)
        self.assertEqual(round(sankoff.tree.data.dictionary["T"], 0), 8)

    def test_backward_pass(self):
        sankoff = Sankoff(self.newick, self.distance_matrix, self.mapping)
        sankoff.do_sankoff()
        self.assertEqual(sankoff.tree.data.label, "G")
        child_labels = [child.data.label for child in sankoff.tree.children]
        self.assertEqual(child_labels, ["G", "G"])

    def test_sankoff_asymmetric(self):
        newick = "(A,(B,C));"
        distance_matrix = [["A", "B", "C", "D"], np.array([[0, 2, 3, 1], [1, 0, 3, 2], [2, 4, 0, 2], [2, 1, 1, 0]])]
        mapping = {"A": "A", "B": "B", "C": "C", "D": "D"}
        sankoff = Sankoff(newick, distance_matrix, mapping)
        sankoff.do_sankoff()
        self.assertEqual(sankoff.tree.data.label, "A")
        self.assertEqual(round(sankoff.tree.data.dictionary["A"], 0), 3)
        self.assertEqual(round(sankoff.tree.data.dictionary["B"], 0), 4)
        self.assertEqual(round(sankoff.tree.data.dictionary["C"], 0), 6)
        self.assertEqual(round(sankoff.tree.data.dictionary["D"], 0), 4)
        child_labels = sorted([child.data.label for child in sankoff.tree.children])
        self.assertEqual(child_labels, ["A", "D"])


if __name__ == '__main__':
    unittest.main()
