from tree import Node
import re
import unittest


class NewickParser:
    """
    A class used to parse a Newick String and generate a tree from it.

    Attributes
    ----------
    input : String
        The Newick String, which is to be parsed
    root : Node
        The root node of the parsed tree

    Methods
    -------
    parse()
        parses a Newick string
    """
    def __init__(self, input):
        """
        Parameters
        ----------
        input : String
            The Newick String, which is to be parsed
        """
        self.input = input
        self.root = None

    def get_split_input(self, input):
        """
        Splits the input Newick String into subparts.

        Parameters
        ----------
        input : String
            The Newick String, which is to be parsed
        """
        indices = []
        counter = 0
        indices.append(-1)
        for i in range(0, len(input)):
            if input[i] == "(":
                counter += 1
            elif input[i] == ")":
                counter -= 1
            elif counter == 0 and input[i] == ",":
                indices.append(i)
        indices.append(len(input))
        splits = []
        for i in range(1, len(indices)):
            begin = indices[i - 1] + 1
            end = indices[i]
            split = input[begin:end].strip()
            splits.append(split)
        return splits

    def parse_input(self, input, parent):
        """
        Parses the input Newick String by searching for the label, edge length and children nodes of the currently
        parsed node, creating the node and recursively adding the children of the node.

        Parameters
        ----------
        input : String
            The Newick String, which is to be parsed
        parent : Node
            Parent node of the currently parsed node
        """
        pattern = r"(\((.*)\))?([^:]*)?(:(.*))?"
        match = re.search(pattern, input)

        if match is None:
            return

        label = match.group(3) if match.group(3) != "" else None
        edge_length = float(match.group(5)) if match.group(5) is not None else None
        node = Node(label, parent, edge_length)
        if match.group(2) != "" and match.group(2) is not None:
            for split in self.get_split_input(match.group(2)):
                child = self.parse_input(split, node)
                node.add_child_node(child)
        return node

    def parse(self):
        """
        Parses the input Newick String by calling the function parse_input(input, parent) with a modified version of the
        Newick String, which lacks the semicolon.
        """
        self.root = self.parse_input(self.input[:-1], None)


class TestNewickParser(unittest.TestCase):
    """
    A class to test the class NewickParser.
    """
    def test_parse_single_leaf(self):
        parser = NewickParser("a:3.2;")
        parser.parse()
        self.assertIsNotNone(parser.root)
        if parser.root is None:
            return
        self.assertEqual(parser.root.data, "a")
        self.assertEqual(parser.root.is_leaf(), True)
        self.assertEqual(parser.root.is_root(), True)

    def test_parse_root_with_leaves(self):
        parser = NewickParser("(a:3.2, b, c:2.1)d;")
        parser.parse()
        self.assertIsNotNone(parser.root)
        if parser.root is None:
            return
        self.assertEqual(parser.root.data, "d")
        self.assertEqual(parser.root.is_leaf(), False)
        self.assertEqual(len(parser.root.children), 3)
        self.assertEqual(parser.root.children[0].data, "a")


if __name__ == '__main__':
    unittest.main()
