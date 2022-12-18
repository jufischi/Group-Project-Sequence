from typing import List, Tuple
import geopandas
import airportsdata
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tree import Node
import pycountry


class Airport:
    airport_locations = airportsdata.load("IATA")

    def __init__(self, name: str) -> None:
        self.x = Airport.airport_locations.get(name)["lon"]
        self.y = Airport.airport_locations.get(name)["lat"]
        self.name = name
        country_name = Airport.airport_locations.get(name)["country"]
        self.country = pycountry.countries.get(alpha_2=country_name).alpha_3


class Tree_Visualizer:
    def draw_tree(root: Node, ax: plt.Axes, continent_list: List[str] = []) -> None:
        world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
        if not continent_list:
            world.plot(ax=ax, zorder=1)
        else:
            for continent in continent_list:
                world[world.continent == continent].plot(ax=ax, zorder=1)

        connections = Tree_Visualizer.collect_connections(root)
        for src, dest in connections:
            if (
                world[world.iso_a3 == src.country].continent.isin(continent_list).all() and
                world[world.iso_a3 == dest.country].continent.isin(continent_list).all()
            ):
                arrow = patches.FancyArrowPatch((src.x, src.y), (dest.x, dest.y), mutation_scale=15, arrowstyle="->")
                ax.plot([src.x, dest.x], [src.y, dest.y], " ", color="red", marker="o")
                ax.add_patch(arrow)

    def collect_connections(subtree_rooted_at: Node) -> List[Tuple[Airport, Airport]]:
        result = []
        current_airport = Airport(subtree_rooted_at.data)
        if subtree_rooted_at.is_leaf():
            return []

        for child in subtree_rooted_at.children:
            result.append((current_airport, Airport(child.data)))
            result.extend(Tree_Visualizer.collect_connections(child))

        return result


class TestVisualizer:
    def visualize() -> None:
        root = Node("STR")
        root.add_child("MUC")
        root.add_child("BER")
        root.children[0].add_child("LAX")
        root.children[0].add_child("CGN")
        root.children[1].add_child("MEX")
        root.children[1].add_child("CHS")

        fig, ax = plt.subplots()
        Tree_Visualizer.draw_tree(root, ax, ["Europe"])
        plt.show()


TestVisualizer.visualize()
