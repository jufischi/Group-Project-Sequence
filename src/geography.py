import geopandas
import pandas as pd
import airportsdata
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class xy:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def get_from_airport(self, airport):
        airport_locs = airportsdata.load("IATA")
        self.x = airport_locs.get(airport)["lon"]
        self.y = airport_locs.get(airport)["lat"]

        return self


def create_dict(file):
    """

    :param file:
    :return:
    """
    data = pd.read_csv(file, delimiter="\t", header=0)
    dict_label = {}
    for label, location in zip(data["label"], data["location"]):
        dict_label[label] = location

    return dict_label


def get_locs(airports):
    longitudinal = [xy().get_from_airport(airport).x for airport in airports]
    latitudinal = [xy().get_from_airport(airport).y for airport in airports]
    df = pd.DataFrame({"airport": airports})
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(longitudinal, latitudinal))

    return gdf


def plot_locs(gdf):
    # import world
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    # create graph
    fig, ax = plt.subplots()
    # plot airports
    gdf.plot(ax=ax, marker='o', color='red', markersize=15, zorder=2)
    # plot continents
    world[world.continent == 'North America'].boundary.plot(ax=ax, zorder=1)
    world[world.continent == 'South America'].plot(ax=ax, zorder=1, alpha=0.85)
    # plot countries
    world[world.name == 'Brazil'].plot(ax=ax, zorder=1, color="lightgreen", edgecolor="white", linewidth=0.5)
    # plot lines
    plot_lines(["LAX", "MEX", "MUC"], ["JFK", "JFK", "JFK"], ax)
    # plot via matplotlib
    plt.plot(xy().get_from_airport("THE").x, xy().get_from_airport("THE").y, marker='o', color='forestgreen', markersize=5, zorder=2)


def plot_lines(From, To,ax):
    assert len(From) == len(To)

    for f, t in zip(From, To):
        xy_f = xy().get_from_airport(f)
        xy_t = xy().get_from_airport(t)
        # plt.plot([xy_f.x, xy_t.x], [xy_f.y, xy_t.y], ":", color="red")
        arrow = mpatches.FancyArrowPatch((xy_f.x, xy_f.y), (xy_t.x, xy_t.y), mutation_scale=15, arrowstyle='->')
        ax.add_patch(arrow)


if __name__ == "__main__":
    mapping = create_dict("../data/tipdata.txt")

    df = get_locs(["JFK", "LAX", "MEX"])

    plot_locs(df)
    plt.show()