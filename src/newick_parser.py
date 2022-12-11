from tree import Node
import re
import unittest

class NewickParser:
    def __init__(self, input):
        self.input = input
        self.root = None

    def get_split_input(self, input):
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
        pattern = r"(\((.*)\))?([^:]*)?(:(.*))?"
        match = re.search(pattern, input)

        if match == None:
            return

        label = match.group(3) if match.group(3) != "" else None
        edge_length = float(match.group(5)) if match.group(5) != None else None
        node = Node(label, parent, edge_length)
        if match.group(2) != "" and match.group(2) != None:
            for split in self.get_split_input(match.group(2)):
                child = self.parse_input(split, node)
                node.add_child_node(child)
        return node

    def parse(self):
        self.root = self.parse_input(self.input[:-1], None)

class TestNewickParser(unittest.TestCase):
    def test_parse_single_leaf(self):
        parser = NewickParser("a:3.2;")
        parser.parse()
        self.assertIsNotNone(parser.root)
        if parser.root == None:
            return
        self.assertEqual(parser.root.data, "a")
        self.assertEqual(parser.root.is_leaf(), True)
        self.assertEqual(parser.root.is_root(), True)

    def test_parse_root_with_leaves(self):
        parser = NewickParser("(a:3.2, b, c:2.1)d;")
        parser.parse()
        self.assertIsNotNone(parser.root)
        if parser.root == None:
            return
        self.assertEqual(parser.root.data, "d")
        self.assertEqual(parser.root.is_leaf(), False)
        self.assertEqual(len(parser.root.children), 3)
        self.assertEqual(parser.root.children[0].data, "a")

if __name__ == '__main__':
    unittest.main()
