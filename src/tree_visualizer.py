from typing import List, Tuple
import geopandas
import airportsdata
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tree import Node
import pycountry


class Airport:
    """
    A class used to represent an airport and its location.

    Attributes
    ----------
    x: float
        The longitude of the airport
    y: float
        The latitude of the airport
    name: str
        The name of the airport represented by the IATA code
    country: str
        The country of the airport as the alpha3 string (e.g. "DEU" for Germany)

    Methods
    -------
    """
    airport_locations = airportsdata.load("IATA")

    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name: str
            The name of the airport in its IATA representation
        """
        self.x = Airport.airport_locations.get(name)["lon"]
        self.y = Airport.airport_locations.get(name)["lat"]
        self.name = name
        country_name = Airport.airport_locations.get(name)["country"]
        self.country = pycountry.countries.get(alpha_2=country_name).alpha_3


class Tree_Visualizer:
    """
    A class used to visualize a tree that has airport IATA names as
    the labels of its nodes such that each node can be drawn on a world map.

    Attributes
    ----------

    Methods
    -------
    draw_tree(root: Node, ax: plt.Axes, continent_list: List[str] = [])
        Draws the tree represented by its root node on the given
        mathplotlib.pyplot Axis. This will produce a vector based world map with
        the tree plotted onto it.
    collect_conections(subtree_rooted_at Node)
        Traverses the tree recursively starting on the given node and returns
        all edges of that tree as a list of tuples of two airports.
    """
    def draw_tree(root: Node, ax: plt.Axes, continent_list: List[str] = []) -> None:
        """
        Draws the tree represented by its root node on the given
        mathplotlib.pyplot Axis. This will produce a vector based world map with
        the tree plotted onto it. This method does not call the ax.show()
        method, so that the caller have the opportunity to manipulate the results
        as they like.

        Parameters
        ----------
        root: Node
            The root of the tree to display on the world map
        ax: pyplot.Axes
            The subfigure in which the tree should be displayed
        continent_list: List[str]
            Optional list of continents to display, e.g. "South America". If
            this list is not set or empty, the whole world is displayed.
        """
        world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
        if not continent_list:
            world.plot(ax=ax, zorder=1)
        else:
            for continent in continent_list:
                world[world.continent == continent].plot(ax=ax, zorder=1)

        connections = Tree_Visualizer.collect_connections(root)
        for src, dest in connections:
            if (
                not continent_list or (
                    world[world.iso_a3 == src.country].continent.isin(continent_list).all() and
                    world[world.iso_a3 == dest.country].continent.isin(continent_list).all()
                )
            ):
                arrow = patches.FancyArrowPatch((src.x, src.y), (dest.x, dest.y), mutation_scale=15, arrowstyle="->")
                ax.plot([src.x, dest.x], [src.y, dest.y], " ", color="red", marker="o")
                ax.add_patch(arrow)

    def collect_connections(subtree_rooted_at: Node) -> List[Tuple[Airport, Airport]]:
        """
        Traverses the tree recursively starting on the given node and returns
        all edges of that tree as a list of tuples of two airports.

        As an example, given a tree with three nodes "STR", "FRA" and "MUC" where "STR" is the
        root and "FRA" and "MUC" are two children of the root, this function
        will return a list [(STR, FRA), (STR, MUC)].

        Parameters
        ----------
        subtree_rooted_at: Node
            The root of the subtree to traverse

        Returns
        ----------
        A list of airport tuples
        """
        result = []
        current_airport = Airport(str(subtree_rooted_at.data))
        if subtree_rooted_at.is_leaf():
            return []

        for child in subtree_rooted_at.children:
            result.append((current_airport, Airport(str(child.data))))
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
        Tree_Visualizer.draw_tree(root, ax)
        plt.show()