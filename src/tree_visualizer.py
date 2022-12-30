from typing import List, Tuple
import geopandas
import airportsdata
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from tree import Node
import pycountry

fallback_airports = {
    "US": "LAX",
    "GB": "LHR",
    "FR": "CDG",
    "DE": "MUC",
    "MX": "MEX",
    "HK": "HKG",
    "CA": "YVR"
}


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
        if len(name) == 2:
            if name in fallback_airports:
                name = fallback_airports[name]
            else:
                name = "SYD"
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
    def draw_tree(root: Node, ax: plt.Axes, continent_list: List[str] = [], every: bool = True,
                  num_children: float = np.inf, num_parents: int = 0) -> None:
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
        every: bool
            Optional boolean to specify if every airport or only its country
            should be visualized
        num_children: float
            Optional float value defining how many children should be drawn
        num_parents: int
            Optional int value defining how many parents should be drawn
        """
        world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))

        connections = Tree_Visualizer.collect_connections(root, num_children, num_parents)
        world[world.iso_a3 == connections[0][0].country].plot(ax=ax, color="seagreen", hatch="///",
                                                              edgecolor="maroon", linewidth=1, zorder=1)

        if not continent_list:
            world[world.name!="Antarctica"].to_crs(4326).plot(ax=ax, zorder=0, color="seagreen", edgecolor="gainsboro", linewidth=0.2)
        else:
            for continent in continent_list:
                world[(world.continent == continent) & (world.name!="Antarctica")].plot(ax=ax, zorder=1,
                                                                                        color="seagreen",
                                                                                        edgecolor="gainsboro",
                                                                                        linewidth=0.2)

        if every:
            Tree_Visualizer.plot_connections(connections, ax, world, continent_list)
        else:
            for src, dest in connections:
                src.x = world[world.iso_a3 == src.country].centroid.x
                src.y = world[world.iso_a3 == src.country].centroid.y
                dest.x = world[world.iso_a3 == dest.country].centroid.x
                dest.y = world[world.iso_a3 == dest.country].centroid.y
            Tree_Visualizer.plot_country_connections(connections, ax, world, continent_list)

    def collect_connections(subtree_rooted_at: Node, num_children: float = np.inf, num_parents: int = 0) \
            -> List[Tuple[Airport, Airport]]:
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
        num_children: float
            Optional float value defining how many children should be visited
        num_parents: int
            Optional int value defining how many parents should be visited

        Returns
        ----------
        A list of airport tuples
        """
        result = []
        current_airport = Airport(str(subtree_rooted_at.data))
        if subtree_rooted_at.is_leaf():
            return []

        if num_children:
            for child in subtree_rooted_at.children:
                result.append((current_airport, Airport(str(child.data))))
                result.extend(Tree_Visualizer.collect_connections(child, num_children=num_children-1,
                                                                  num_parents=0))

        if num_parents and not subtree_rooted_at.is_root():
            result.append((Airport(str(subtree_rooted_at.parent.data)), current_airport))
            result.extend(Tree_Visualizer.collect_connections(subtree_rooted_at, num_children=0,
                                                              num_parents=num_parents-1))

        return result

    def create_LineCollection(src: Airport, dest: Airport, n: int = 100) -> LineCollection:
        """
        Creates a LineCollection object, which represents a directed dotted line between two Airports

        Parameters
        ----------
        src: Airport
            source Airport
        dest: Airport
            destination Airport
        n: int
            optional, number of drawn points

        Returns
        ----------
        matplotlib object LineCollection
        """
        # spacing for continuous line
        x = np.linspace(src.x, dest.x, n)
        y = np.linspace(src.y, dest.y, n)
        # create segments
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = [s for i, s in enumerate(np.concatenate([points[:-1], points[1:]], axis=1)) if i % 5 != 0]
        # normalize set start of color scheme
        norm = plt.Normalize(-n / 2, n)
        lc = LineCollection(segments, cmap='Reds', linewidths=1, norm=norm, zorder=2)
        # set which colors should be iterated
        lc.set_array(np.arange(n))
        return lc

    def plot_country_connections(connections: List[Tuple[Airport, Airport]], ax: plt.Axes,
                                 world: geopandas.geodataframe.GeoDataFrame, continents: List[str] = []) -> None:
        """
        Draws connections between Airports. The location of each airport is centered in the corresponding country.
        All connections within one country are therefore not visible.

        As an example, the airport MUC (Munich) will be displayed in the center of Germany.

        Parameters
        ----------
        connections: List[Tuple[Airport, Airport]]
            A connection from one Airport to its destination Airport
        ax: pyplot.Axes
            The subfigure in which the tree should be displayed
        world: geopandas.geodataframe.GeoDataFrame
            GeoDataFrame containing the information of a world map
        continents: List[str] = []
            Optional list of continents to display, e.g. "South America". If
            this list is not set or empty, the whole world is displayed.

        Returns
        ----------
        matplotlib object LineCollection
        """
        countries = set()
        for src, dest in connections:
            if (
                    not continents or (
                    world[world.iso_a3 == src.country].continent.isin(continents).all() and
                    world[world.iso_a3 == dest.country].continent.isin(continents).all()
            )
            ):
                if (src.country not in countries or dest.country not in countries) and src.country != dest.country:
                    countries.add(src.country)
                    countries.add(dest.country)
                    ax.plot([src.x, dest.x], [src.y, dest.y], " ", color="red", marker="o", markersize=5, zorder=3)
                    ax.add_collection(Tree_Visualizer.create_LineCollection(src, dest))
                else:
                    continue

    def plot_connections(connections: List[Tuple[Airport, Airport]], ax: plt.Axes,
                                 world: geopandas.geodataframe.GeoDataFrame, continents: List[str] = []) -> None:
        """
        Draws connections between Airports. The location of each airport is centered in the corresponding country.
        All connections within one country are therefore not visible.

        As an example, the airport MUC (Munich) will be displayed in the center of Germany.

        Parameters
        ----------
        connections: List[Tuple[Airport, Airport]]
            A connection from one Airport to its destination Airport
        ax: pyplot.Axes
            The subfigure in which the tree should be displayed
        world: geopandas.geodataframe.GeoDataFrame
            GeoDataFrame containing the information of a world map
        continents: List[str] = []
            Optional list of continents to display, e.g. "South America". If
            this list is not set or empty, the whole world is displayed.

        Returns
        ----------
        matplotlib object LineCollection
        """
        for src, dest in connections:
            if (
                    not continents or (
                    world[world.iso_a3 == src.country].continent.isin(continents).all() and
                    world[world.iso_a3 == dest.country].continent.isin(continents).all()
            )
            ):
                ax.plot([src.x, dest.x], [src.y, dest.y], " ", color="red", marker="o", markersize=5, zorder=3)
                ax.add_collection(Tree_Visualizer.create_LineCollection(src, dest))

        ax.plot(connections[0][0].x, connections[0][0].y, color="maroon", marker="o", markersize=5, zorder=3)



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
        Tree_Visualizer.draw_tree(root.children[1], ax, [], True, num_children=10, num_parents=10)
        plt.show()
