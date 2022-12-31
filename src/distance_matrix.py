import numpy as np
import unittest


class DistanceMatrix:
    """
    A class used to represent a distance matrix.

    Attributes
    ----------
    header : list of str, optional
        A list of string values associated with each column in the distance matrix
    matrix : 2D numpy.array, optional
        A square matrix containing all distances between every member of header

    Methods
    -------
    read_matrix(file, delimiter=",")
        reads in a matrix from a file. The kind of delimiter is optional
    set_distance_matrix(header, matrix)
        sets class properties header and matrix
    get_distance(id_from, id_to)
        returns distance between two elements in header
    get_header()
        returns list of header names
    set_header(names)
        sets header names
    get_size()
        returns size of square matrix
    """

    def __init__(self, data=None, delimiter=","):
        """

        :param data:
        :param delimiter:
        :return:
        """
        if type(data) == str:
            self.read_matrix(data, delimiter)
        elif type(data) == list:
            self.set_distance_matrix(header=data[0], matrix=data[1])
        else:
            self.header = None
            self.matrix = None

    def read_matrix(self, file, delimiter=","):
        """
        reads in a matrix from a file. The kind of delimiter is optional

        :param file: str, file path
        :param delimiter: str, delimiter (optional)
        """
        header = np.array([x.replace("\"", "") for x in np.genfromtxt(
            file,
            dtype=str,
            delimiter=delimiter,
            max_rows=1,
            autostrip=True
            )[1:]])
        matrix = np.genfromtxt(
            file,
            dtype=float,
            delimiter=delimiter,
            skip_header=1,
            usecols=np.arange(1, len(header) + 1)
            )

        self.set_distance_matrix(header, matrix)

    def set_distance_matrix(self, header, matrix):
        """
        sets class properties header and matrix

        :param header: list of str, column names
        :param matrix: 2D numpy.array, distance matrix
        """
        self.header = header
        self.matrix = matrix
        header_keys = {}
        for i in range(len(self.header)):
            header_keys[self.header[i]] = i
        self.header_keys = header_keys

    def get_distance(self, header_from, header_to):
        """
        returns distance between two elements in header

        :param header_from: str, row name
        :param header_to: str, column name
        :return: float, distance
        """
        return self.matrix[self.header_keys[header_from], self.header_keys[header_to]]

    def get_distance_from_index(self, id_from, id_to):
        """
        returns distance between two elements in header

        :param id_from: integer, row id
        :param id_to: integer, column id
        :return: float, distance
        """
        return self.matrix[id_from, id_to]

    def get_header(self):
        """
        returns list of header names

        :return: list of str, header names
        """
        return self.header

    def set_header(self, names):
        """

        :param names:
        :return:
        """

        self.header = names

    def get_size(self):
        """
        returns size of square matrix

        :return: int, size of matrix
        """
        return self.matrix.size


class TestDistanceMatrix(unittest.TestCase):
    """
    A class to test the class Distance_matrix.
    """

    def test_get_distance(self):
        m = DistanceMatrix()
        m.set_distance_matrix(header=np.array(["a", "b"]), matrix=np.array([[1, 2], [3, 4]]))
        self.assertEqual(m.get_distance(header_from="a", header_to="b"), 2)

    def test_get_size(self):
        m = DistanceMatrix(data=[np.array(["a", "b"]), np.array([[1, 2], [3, 4]])])
        self.assertEqual(m.get_size(), 4)

    def test_get_header(self):
        m = DistanceMatrix()
        m.set_distance_matrix(header=np.array(["c", "d"]), matrix=np.array([[1, 2], [3, 4]]))
        m.set_header(["a", "b"])
        self.assertTrue(np.array_equal(m.get_header(), np.array(["a", "b"])))


if __name__ == '__main__':
    unittest.main()
