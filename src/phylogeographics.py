from newick_parser import NewickParser
from tree_visualizer import Tree_Visualizer
from matplotlib import pyplot as plt
from sankoff import Sankoff
import airportsdata
import os


class AirportTipMapper:
    """
    A class to map the tips of a given phylogenetic tree to airports.
    """
    def __init__(self, tip_file_path: str) -> None:
        self.data = {}
        with open(tip_file_path, "r") as file:
            for line in file.readlines()[1:]:
                items = line.split("\t")
                self.data[items[0]] = items[1].strip()


class CountryTipMapper:
    """
    A class to map the tips of a given phylogenetic tree to countries.
    """
    def __init__(self, tip_file_path: str) -> None:
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
        countryMapper = CountryTipMapper(os.path.join(cwd, "data", "tipdata.txt"))
        airportMapper = AirportTipMapper(os.path.join(cwd, "data", "tipdata.txt"))
        variants = [
            ("geographic.distance.matrix.csv", "airport_geographic", airportMapper),
            ("effective.distance.matrix.csv", "airport_effective", airportMapper),
            ("geographic.distance.matrix.country.csv", "country_geographic", countryMapper),
            ("effective.distance.matrix.country.csv", "country_effective", countryMapper)
        ]

        for variant_matrix_name, variant_name, variant_mapper in variants:
            print(f"current variant: {variant_name}")
            variant_file_path = os.path.join(cwd, "data", f"{variant_name}.txt")
            variant_tree = None
            if os.path.exists(variant_file_path):
                print(f"variant file {variant_file_path} found, reusing...")
                with open(variant_file_path, "r") as variant_file:
                    variant_newick = variant_file.readlines()[0]
                    parser = NewickParser(variant_newick)
                    parser.parse()
                    variant_tree = parser.root
            else:
                print(f"variant file {variant_file_path} not found, performing Sankoff...")
                sankoff = Sankoff(newick_string, os.path.join(cwd, "data", variant_matrix_name), variant_mapper.data)
                sankoff.perform_sankoff()
                with open(variant_file_path, "w") as variant_file:
                    variant_file.writelines(sankoff.tree.get_newick())
                variant_tree = sankoff.tree

            fig, ax = plt.subplots()
            Tree_Visualizer.draw_tree(variant_tree, ax, [])
            plt.show()


if __name__ == '__main__':
    main()
