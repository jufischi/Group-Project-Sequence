from tree_visualizer import TreeVisualizer
from matplotlib import pyplot as plt
from newick_parser import NewickParser
from phylogeographics import AirportTipMapper
import os
from tree_visualizer import Airport
import matplotlib as mpl


def main() -> None:
    cwd = ".."
    with open(os.path.join(cwd, "data", "pH1N1_until_20093004_cds_rooted.labeled.phy"), "r"):
        airport_mapper = AirportTipMapper(os.path.join(cwd, "data", "tipdata.txt"))
        variants = [
            ("geographic.distance.matrix.csv", "airport_geographic", airport_mapper),
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

            tree_labels = [(Airport('MEX'), Airport('MEX')),
                           (Airport('MEX'), Airport('DAL')),
                           (Airport('DAL'), Airport('ELD')),
                           (Airport('ELD'), Airport('ELD')),
                           (Airport('ELD'), Airport('ELD')),
                           (Airport('ELD'), Airport('JBR')),
                           (Airport('JBR'), Airport('JBR')),
                           (Airport('JBR'), Airport('JBR')),
                           (Airport('JBR'), Airport('JBR')),
                           (Airport('JBR'), Airport('JBR')),
                           (Airport('JBR'), Airport('JBR')),
                           (Airport('JBR'), Airport('JBR')),
                           (Airport('JBR'), Airport('LNS')),
                           (Airport('LNS'), Airport('MUC')),
                           (Airport('MUC'), Airport('MUC'))]

            connections = []
            tree = variant_tree
            for i, label in enumerate(tree_labels):
                for a in [0.2, 1]:
                    fig, ax = plt.subplots()
                    ax.set_xlim(-130, 25)
                    ax.set_ylim(5, 90)
                    TreeVisualizer.draw_tree(variant_tree, ax, map=False)

                    for src, dest in tree_labels[0:i]:
                        ax.plot([src.x, dest.x], [src.y, dest.y], "-", color="blue", marker="o", markersize=3,
                                zorder=3, alpha=a)

                    for src, dest in connections:
                        ax.plot([src.x, dest.x], [src.y, dest.y], "-", color="blue", marker="o", markersize=3,
                                    zorder=2, alpha=0.2)
                    plt.show()

                # end
                new_connections = TreeVisualizer.collect_connections(tree, num_children=1)
                connections.extend(new_connections)
                for child in tree.children:
                    if child.data == tree_labels[i][1].name:
                        tree = child


            #fig.subplots_adjust(bottom=0.15, hspace=-0.175, wspace=0.075)
            #plt.savefig(os.path.join(cwd, "doc", variant_name + "_europe.pdf"), dpi=150)


if __name__ == '__main__':
    main()
