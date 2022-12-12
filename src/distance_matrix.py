import numpy as np
import unittest


class Distance_matrix:
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
        header = np.genfromtxt(file, dtype=str, delimiter=delimiter, max_rows=1, autostrip=True)[1:]
        matrix = np.genfromtxt(file, dtype=float, delimiter=delimiter, skip_header=1, usecols=np.arange(1, len(header)+1))

        self.set_distance_matrix(header, matrix)

    def set_distance_matrix(self, header, matrix):
        """
        sets class properties header and matrix

        :param header: list of str, column names
        :param matrix: 2D numpy.array, distance matrix
        """
        assert len(header) == matrix[0, :].size == matrix[:, 0].size

        self.header = header
        self.matrix = matrix

    def get_distance(self, id_from, id_to):
        """
        returns distance between two elements in header

        :param id_from: str, row name
        :param id_to: str, column name
        :return: float, distance
        """
        assert id_from in self.header and id_to in self.header

        return self.matrix[self.header.index(id_from), self.header.index(id_to)]

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
        assert len(names) == self.matrix[0, :].size

        self.header = names

    def get_size(self):
        """
        returns size of square matrix

        :return: int, size of matrix
        """
        return self.matrix.size


class Test_distance_matrix(unittest.TestCase):
    """
    A class to test the class Distance_matrix.
    """

    def test_get_distance(self):
        m = Distance_matrix()
        m.set_distance_matrix(header=["a", "b"], matrix=np.array([[1, 2], [3, 4]]))
        self.assertEqual(m.get_distance(id_from="a", id_to="b"), 2)

    def test_get_size(self):
        m = Distance_matrix(data=[["a", "b"], np.array([[1, 2], [3, 4]])])
        self.assertEqual(m.get_size(), 4)

    def test_get_header(self):
        m = Distance_matrix()
        m.set_distance_matrix(header=["c", "d"], matrix=np.array([[1, 2], [3, 4]]))
        m.set_header(["a", "b"])
        self.assertEqual(m.get_header(), ["a", "b"])


if __name__ == '__main__':
    unittest.main()