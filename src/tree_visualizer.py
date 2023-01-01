from typing import List, Tuple
import geopandas
import airportsdata
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from tree import Node
import pycountry
from mpl_toolkits.axes_grid1 import make_axes_locatable

country_airports = {
    "US": "LAX",
    "GB": "LHR",
    "FR": "CDG",
    "DE": "MUC",
    "MX": "MEX",
    "HK": "HKG",
    "CA": "YVR",
    "NZ": "AKL",
    "BR": "GIG",
    "CR": "SJO",
    "SV": "SAL",
    "DO": "JBQ",
    "KR": "ICN",
    "SE": "ARN",
    "ES": "MAD"
}

lam_airport = {
    "icao": "KLAM",
    "iata": "LAM",
    "name": "Los Alamos Airport",
    "city": "Los Alamos",
    "subd": "New Mexico",
    "country": "US",
    "elevation": 7170.9,
    "lat": 35.8796861111111,
    "lon": -106.268686111111,
    "tz": "America/Denver",
    "tz": "America/Denver",
    "lid": "LAM"
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
    airport_locations["LAM"] = lam_airport

    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name: str
            The name of the airport in its IATA representation
        """
        if len(name) == 2 or Airport.airport_locations.get(name) is None:
            if name in country_airports:
                name = country_airports[name]
            else:
                print(f"location {name} not found")
                name = "SYD"
        self.x = Airport.airport_locations.get(name)["lon"]
        self.y = Airport.airport_locations.get(name)["lat"]
        self.name = name
        country_name = Airport.airport_locations.get(name)["country"]
        self.country = pycountry.countries.get(alpha_2=country_name).alpha_3


class TreeVisualizer:
    """
    A class used to visualize a tree that has airport IATA names as
    the labels of its nodes such that each node can be drawn on a world map.

    Attributes
    ----------

    Methods
    -------
    draw_tree(root: Node, ax: plt.Axes, continent_list: List[str] = [])
        Draws the tree represented by its root node on the given
        matplotlib.pyplot Axis. This will produce a vector based world map with
        the tree plotted onto it.
    collect_connections(subtree_rooted_at Node)
        Traverses the tree recursively starting on the given node and returns
        all edges of that tree as a list of tuples of two airports.
    """
    def draw_tree(root: Node, fig: plt.Figure, ax: plt.Axes, continent_list: List[str] = [], every: bool = True,
                  num_children: float = np.inf, num_parents: int = 0, n: int = 100) -> None:
        """
        Draws the tree represented by its root node on the given
        matplotlib.pyplot Axis. This will produce a vector based world map with
        the tree plotted onto it. This method does not call the ax.show()
        method, so that the caller have the opportunity to manipulate the results
        as they like.

        Parameters
        ----------
        root: Node
            The root of the tree to display on the world map
        fig: pyplot.Figure
            Figure containing all subfigures
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
        n: int
            optional, number of drawn points between one connection
        """
        world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))

        connections = TreeVisualizer.collect_connections(root, num_children, num_parents)
        world[world.iso_a3 == connections[0][0].country].plot(ax=ax, color="seagreen", hatch="///",
                                                              edgecolor="maroon", linewidth=1, zorder=1)

        if not continent_list:
            world[world.name != "Antarctica"].to_crs(4326).plot(ax=ax, zorder=0, color="seagreen",
                                                                edgecolor="gainsboro", linewidth=0.2)
        else:
            for continent in continent_list:
                world[(world.continent == continent) & (world.name != "Antarctica")].plot(ax=ax, zorder=1,
                                                                                          color="seagreen",
                                                                                          edgecolor="gainsboro",
                                                                                          linewidth=0.2)

        if every:
            lc = TreeVisualizer.plot_connections(connections, ax, world, continent_list)
        else:
            for src, dest in connections:
                src.x = world[world.iso_a3 == src.country].centroid.x
                src.y = world[world.iso_a3 == src.country].centroid.y
                dest.x = world[world.iso_a3 == dest.country].centroid.x
                dest.y = world[world.iso_a3 == dest.country].centroid.y
            lc = TreeVisualizer.plot_country_connections(connections, ax, world, continent_list)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="4%", pad=0.04)
        cbar = fig.colorbar(lc, ax=ax, cax=cax)
        cbar.ax.get_yaxis().set_ticks([-n / 2, n], labels=["src", "dest"])

    def draw_path_to_root(root: Node, label: str, fig: plt.Figure, ax: plt.Axes, continent_list: List[str] = [],
                          every: bool = True, num_children: float = np.inf, num_parents: int = 0, n: int = 100):
        """
        Prunes the given tree to only contain all paths from a given label to the root. Then calls upon the
        draw_tree() function to draw the pruned tree. This function destroys the tree object.

        Parameters
        ----------
        root: Node
            The root of the tree to display on the world map
        label: String
            label of nodes for which we want the pruned subtree
        fig: pyplot.Figure
            Figure containing all subfigures
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
        n: int
            optional, number of drawn points between one connection
        """

        def prune_tree(node: Node, label: str):
            """
            Internal function to prune the tree to only contain all paths from a given label to the root.

            Parameters
            ----------
            node: Node
                The root of the tree to be pruned
            label: String
                label of nodes for which we want the pruned subtree
            """
            for child in node.children[:]:
                prune_tree(child, label)
            if str(node.data) != label and len(node.children) == 0:
                parent = node.parent
                parent.prune_child(node)

        prune_tree(root, label)  # prune tree
        # run visualizer using pruned tree:
        TreeVisualizer.draw_tree(root, fig, ax, continent_list, every, num_children, num_parents, n)

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
                result.extend(TreeVisualizer.collect_connections(child, num_children=num_children - 1,
                                                                 num_parents=0))

        if num_parents and not subtree_rooted_at.is_root():
            result.append((Airport(str(subtree_rooted_at.parent.data)), current_airport))
            result.extend(TreeVisualizer.collect_connections(subtree_rooted_at, num_children=0,
                                                             num_parents=num_parents-1))

        return result

    def create_line_collection(src: Airport, dest: Airport, n: int = 100) -> LineCollection:
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
                                 world: geopandas.geodataframe.GeoDataFrame, continents: List[str] = [],
                                 n: int = 100) -> LineCollection:
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
        n: int
            optional, number of drawn points for each line

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
                    lc = TreeVisualizer.create_line_collection(src, dest, n)
                    ax.add_collection(lc)
                else:
                    continue
        return lc

    def plot_connections(connections: List[Tuple[Airport, Airport]], ax: plt.Axes,
                         world: geopandas.geodataframe.GeoDataFrame, continents: List[str] = [],
                         n: int = 100) -> LineCollection:
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
        n: int
            optional, number of drawn points for each line

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
                lc = TreeVisualizer.create_line_collection(src, dest, n)
                ax.add_collection(lc)

        ax.plot(connections[0][0].x, connections[0][0].y, color="maroon", marker="o", markersize=5, zorder=4)
        return lc


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
        TreeVisualizer.draw_tree(root.children[1], fig, ax, [], False, num_children=10, num_parents=10)
        plt.show()
