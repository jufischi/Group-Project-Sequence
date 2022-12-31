from newick_parser import NewickParser
from distance_matrix import DistanceMatrix
import unittest
import numpy as np


class Sankoff:
    """
    A class used to parse a Newick String and generate a tree from it.

    Attributes
    ----------
    newick_string : String
        The Newick String for the tree that Sankoff is performed on
    distance_matrix : list / String
        The distance matrix in form of a list / path to csv file containing the distance matrix
    mapping : dictionary
        The mapping of node labels to locations
    delimiter : String
        The delimiter used in the distance matrix

    Methods
    -------
    perform_sankoff()
        performs Sankoff algorithm on the given tree and distance matrix
    """
    def __init__(self, newick_string, distance_matrix, mapping, delimiter=','):
        """
        Parameters
        ----------
        newick_string : String
            The Newick String for the tree that Sankoff is performed on
        distance_matrix : list / String
            The distance matrix in form of a list / path to csv file containing the distance matrix
        mapping : dictionary
            The mapping of node labels to locations
        delimiter : String
            The delimiter used in the distance matrix
        """
        parser = NewickParser(newick_string)
        parser.parse()
        self.tree = parser.root

        self.distance_matrix = DistanceMatrix(distance_matrix, delimiter)
        self.mapping = mapping

        self._set_tree_labels(self.tree)

    def perform_sankoff(self):
        """
        Performs the Sankoff algorithm on the given tree and distance matrix by calling the functions
        _forward_pass(tree) and _backward_pass(tree). Does not require any input.
        """
        self._forward_pass(self.tree)
        self._backward_pass(self.tree)

    def _set_tree_labels(self, node):
        """
        Recursive function to set all tree labels as an object TreeLabel.

        Parameters
        ----------
        node : Node
            Currently worked on node
        """
        for child in node.children:
            self._set_tree_labels(child)
        if node.is_leaf():
            label = self.mapping[node.data]
            dictionary = dict([(x, 0) if x == label else (x, float('inf')) for x in self.distance_matrix.header])
            node.data = TreeLabel(label, node.data, dictionary)
        else:
            node.data = TreeLabel(None, node.data, {})

    def _forward_pass(self, node):
        """
        Function to perform the forward pass of the Sankoff algorithm. Starting from the leaves, this function
        calculates the cost at each node for any given label.

        Parameters
        ----------
        node : Node
            Currently worked on node

        Returns
        -------
        dict
            with key = label and value = cost for the given node
        """
        list_of_dict = []
        for child in node.children:
            list_of_dict.append(self._forward_pass(child))
        if not node.is_leaf():
            for label in self.distance_matrix.header:
                cost = 0
                for child in list_of_dict:
                    cost += min([(value + self.distance_matrix.get_distance(label, key))
                                 for key, value in child.items()])
                node.data.dictionary[label] = cost
        return node.data.dictionary

    def _backward_pass(self, node):
        """
        Function to perform the backward pass of the Sankoff algorithm. Starting from the root, this function assigns
        the appropriate label to the node.

        Parameters
        ----------
        node : Node
            Currently worked on node
        """
        node.data.label, _ = self._get_minimal_cost(node)
        for child in node.children:
            self._backward_pass(child)

    def _get_minimal_cost(self, node):
        """
        Returns the minimal cost at a given node and the corresponding label.

        Parameters
        ----------
        node : Node
            Currently worked on node

        Returns
        -------
        key : String
            label for which the cost is minimal
        min_cost : int
            minimal cost
        """
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
    """
    A class to store the information about a node in the tree

    Attributes
    ----------
    label : String
        information about the location (airport or country)
    info : String
        additional information about the node (e.g. sequence ID)
    dictionary : dict
        stores cost at each node and node label for computation of Sankoff
    """
    def __init__(self, label, info, dictionary):
        self.label = label
        self.info = info
        self.dictionary = dictionary

    def __str__(self):
        return str(self.label)


class TestSankoff(unittest.TestCase):
    """
    A class to test the class Sankoff.
    """
    def setUp(self):
        self.newick = "(((A,C),G),(C,G));"
        self.distance_matrix = [["A", "C", "G", "T"],
                                np.array([[0, 2, 1, 2], [2, 0, 2, 1], [1, 2, 0, 2], [2, 1, 2, 0]])]
        self.mapping = {"A": "A", "C": "C", "G": "G", "T": "T"}

    def test_forward_pass(self):
        sankoff = Sankoff(self.newick, self.distance_matrix, self.mapping)
        sankoff._forward_pass(sankoff.tree)
        self.assertEqual(round(sankoff.tree.data.dictionary["A"], 0), 6)
        self.assertEqual(round(sankoff.tree.data.dictionary["C"], 0), 6)
        self.assertEqual(round(sankoff.tree.data.dictionary["G"], 0), 5)
        self.assertEqual(round(sankoff.tree.data.dictionary["T"], 0), 8)

    def test_backward_pass(self):
        sankoff = Sankoff(self.newick, self.distance_matrix, self.mapping)
        sankoff.perform_sankoff()
        self.assertEqual(sankoff.tree.data.label, "G")
        child_labels = [child.data.label for child in sankoff.tree.children]
        self.assertEqual(child_labels, ["G", "G"])

    def test_sankoff_asymmetric(self):
        newick = "(A,(B,C));"
        distance_matrix = [["A", "B", "C", "D"], np.array([[0, 2, 3, 1], [1, 0, 3, 2], [2, 4, 0, 2], [2, 1, 1, 0]])]
        mapping = {"A": "A", "B": "B", "C": "C", "D": "D"}
        sankoff = Sankoff(newick, distance_matrix, mapping)
        sankoff.perform_sankoff()
        self.assertEqual(sankoff.tree.data.label, "A")
        self.assertEqual(round(sankoff.tree.data.dictionary["A"], 0), 3)
        self.assertEqual(round(sankoff.tree.data.dictionary["B"], 0), 4)
        self.assertEqual(round(sankoff.tree.data.dictionary["C"], 0), 6)
        self.assertEqual(round(sankoff.tree.data.dictionary["D"], 0), 4)
        child_labels = sorted([child.data.label for child in sankoff.tree.children])
        self.assertEqual(child_labels, ["A", "D"])


if __name__ == '__main__':
    unittest.main()
