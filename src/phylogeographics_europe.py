from tree_visualizer import TreeVisualizer
from matplotlib import pyplot as plt
from newick_parser import NewickParser
from phylogeographics import AirportTipMapper
import os
import matplotlib as mpl


def main() -> None:
    cwd = ".."
    with open(os.path.join(cwd, "data", "pH1N1_until_20093004_cds_rooted.labeled.phy"), "r"):
        airport_mapper = AirportTipMapper(os.path.join(cwd, "data", "tipdata.txt"))
        variants = [
            ("geographic.distance.matrix.csv", "airport_geographic", airport_mapper),
            ("effective.distance.matrix.csv", "airport_effective", airport_mapper),
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
                print(f"variant file {variant_file_path} not found, please perform Sankoff")

            europe = ['DEU', 'ESP', 'SWE', 'GBR']
            titles = ['(a) Germany', '(b) Spain', '(c) Sweden', '(d) United Kingdom']

            mpl.rcParams['font.family'] = 'Times New Roman'
            fig, axes = plt.subplots(2, 2)
            for country, ax, title in zip(europe, axes.flat, titles):
                TreeVisualizer.draw_path_to_root(variant_tree, country, ax)
                ax.set_xlim(-130, 25)
                ax.set_ylim(5, 90)
                ax.set_title(title, loc='left', y=0.9)

            fig.subplots_adjust(bottom=0.15, hspace=-0.175, wspace=0.075)
            norm = mpl.colors.Normalize(-100 / 2, 100)
            cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap="Reds"), cax=plt.axes([0.25, 0.1, 0.5, 0.025]),
                                orientation='horizontal')
            cbar.ax.get_xaxis().set_ticks([-100 / 2, 100], labels=["src", "dest"])
            cbar.outline.set_visible(False)

            plt.savefig(os.path.join(cwd, "doc", variant_name + "_europe.pdf"), dpi=150)
            plt.show()


if __name__ == '__main__':
    main()
