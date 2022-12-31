from tree_visualizer import TreeVisualizer
from matplotlib import pyplot as plt
from sankoff import Sankoff
# import airportsdata
import os


class TipMapper:
    def __init__(self, tip_file_path: str) -> None:
        self.data = {}
        # airports = airportsdata.load("IATA")
        with open(tip_file_path, "r") as file:
            for line in file.readlines()[1:]:
                items = line.split("\t")
                self.data[items[0]] = items[1].strip()  # airports.get(items[1].strip())["country"]


def main() -> None:
    cwd = ".."
    with open(os.path.join(cwd, "data", "pH1N1_until_20093004_cds_rooted.labeled.phy"), "r") as file:
        newick_string = file.readlines()[0]

        mapper = TipMapper(os.path.join(cwd, "data", "tipdata.txt"))
        sankoff = Sankoff(newick_string, os.path.join(cwd, "data", "geographic.distance.matrix.csv"), mapper.data)
        sankoff.perform_sankoff()

        fig, ax = plt.subplots()
        TreeVisualizer.draw_tree(sankoff.tree, ax, [])
        plt.show()


if __name__ == '__main__':
    main()
