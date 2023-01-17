from tree_visualizer import TreeVisualizer
from matplotlib import pyplot as plt
from newick_parser import NewickParser
from phylogeographics import AirportTipMapper, CountryTipMapper
import os
import matplotlib as mpl


def main() -> None:
    cwd = ".."
    with open(os.path.join(cwd, "data", "pH1N1_until_20093004_cds_rooted.labeled.phy"), "r"):
        country_mapper = CountryTipMapper(os.path.join(cwd, "data", "tipdata.txt"))
        airport_mapper = AirportTipMapper(os.path.join(cwd, "data", "tipdata.txt"))
        variants = [
            (0, "geographic.distance.matrix.csv", "airport_geographic", airport_mapper),
            (1, "effective.distance.matrix.csv", "airport_effective", airport_mapper),
            (2, "geographic.distance.matrix.country.csv", "country_geographic", country_mapper),
            (3, "effective.distance.matrix.country.csv", "country_effective", country_mapper)
        ]

        mpl.rcParams['font.family'] = 'Times New Roman'
        for idx, variant_matrix_name, variant_name, variant_mapper in variants:
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
                print(f"variant file {variant_file_path} not found, please perform Sankoff")

            title = ['(a) geographic distances', '(b) effective distances']
            if idx % 2 == 0:
                fig, ax = plt.subplots(2, 1)
            TreeVisualizer.draw_tree(variant_tree, ax[idx % 2], every=False, color="")
            ax[idx % 2].set_title(title[idx % 2], loc='left', y=0.95)

            if idx % 2 == 1:
                fig.subplots_adjust(bottom=0.15, hspace=0.1)
                norm = mpl.colors.Normalize(-100 / 2, 100)
                cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap="Reds"), cax=plt.axes([0.25, 0.1, 0.5, 0.025]),
                                    orientation='horizontal')
                cbar.ax.get_xaxis().set_ticks([-100 / 2, 100], labels=["src", "dest"])
                cbar.outline.set_visible(False)

                plt.savefig(os.path.join(cwd, "doc", variant_name + "_country.pdf"), dpi=150)
                plt.show()


if __name__ == '__main__':
    main()
