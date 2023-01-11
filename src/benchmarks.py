from sankoff import Sankoff
import airportsdata
import os


class AirportTipMapper:
    """
    A class used to read a file containing tip mapping from label to airport and generating a dictionary from the data.

    Attributes
    ----------
    tip_file_path : String
        The path to the file containing the tip mapping from label to airport
    """
    def __init__(self, tip_file_path: str) -> None:
        """
        Parameters
        ----------
        tip_file_path : String
            The path to the file containing the tip mapping from label to airport
        """
        self.data = {}
        with open(tip_file_path, "r") as file:
            for line in file.readlines()[1:]:
                items = line.split("\t")
                self.data[items[0]] = items[1].strip()


class CountryTipMapper:
    """
    A class used to read a file containing tip mapping from label to airport and
    generating a dictionary that maps the tip data to the countries of the airports.

    Attributes
    ----------
    tip_file_path : String
        The path to the file containing the tip mapping from label to airport
    """
    def __init__(self, tip_file_path: str) -> None:
        """
        Parameters
        ----------
        tip_file_path : String
            The path to the file containing the tip mapping from label to airport
        """
        self.data = {}
        airports = airportsdata.load("IATA")
        with open(tip_file_path, "r") as file:
            for line in file.readlines()[1:]:
                items = line.split("\t")
                self.data[items[0]] = airports.get(items[1].strip())["country"]


def main() -> None:
    cwd = ".."
    with open(os.path.join(cwd, "data", "pH1N1_until_20093004_cds_rooted.labeled.phy"), "r") as file:
        newick_string = file.readlines()[0]
        country_mapper = CountryTipMapper(os.path.join(cwd, "data", "tipdata.txt"))
        airport_mapper = AirportTipMapper(os.path.join(cwd, "data", "tipdata.txt"))
        variants = [
            ("geographic.distance.matrix.csv", "airport_geographic", airport_mapper),
            ("effective.distance.matrix.csv", "airport_effective", airport_mapper),
            ("geographic.distance.matrix.country.csv", "country_geographic", country_mapper),
            ("effective.distance.matrix.country.csv", "country_effective", country_mapper)
        ]

        variant_matrix_name, _, variant_mapper = variants[0]
        sankoff = Sankoff(newick_string, os.path.join(cwd, "data", variant_matrix_name), variant_mapper.data)
        sankoff.perform_sankoff()


if __name__ == '__main__':
    main()
