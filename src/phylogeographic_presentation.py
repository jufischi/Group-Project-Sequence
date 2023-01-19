from tree_visualizer import TreeVisualizer
from matplotlib import pyplot as plt
import os
from tree_visualizer import Airport
from tree import Node


def main() -> None:
    cwd = ".."
    first = [(Airport('MEX'), Airport('DAL')),
             (Airport('MEX'), Airport('ELD')),
             (Airport('MEX'), Airport('LAX')),
             (Airport('MEX'), Airport('SAB'))]
    second = [(Airport('DAL'), Airport('JFK')),
              (Airport('DAL'), Airport('ATA')),
              (Airport('DAL'), Airport('OBI')),
              (Airport('DAL'), Airport('RAE'))]
    third = [(Airport('JFK'), Airport('YYZ')),
             (Airport('JFK'), Airport('AMD')),
             (Airport('JFK'), Airport('TAI')),
             (Airport('JFK'), Airport('WIC'))]
    fourth = [(Airport('YYZ'), Airport('STR')),
              (Airport('YYZ'), Airport('ABU')),
              (Airport('YYZ'), Airport('BUR')),
              (Airport('YYZ'), Airport('ABI'))]

    travel = [first, second, third, fourth]

    route = []
    x = 80
    y = 45
    center = (first[0][0].x, first[0][0].y)
    for idx, t in enumerate(travel):
        fig, ax = plt.subplots(figsize=(8, 4.5))
        TreeVisualizer.draw_tree(Node, ax, map=False)

        i = 0
        route.extend(t)
        ax.plot(center[0], center[1], "", color="tomato", marker="o", markersize=3, zorder=4)
        for src, dest in route:
            if i % 4 == 0 and idx < 4:
                ax.plot([src.x, dest.x], [src.y, dest.y], "-", color="blue", marker="o", markersize=3, zorder=3)
            else:
                ax.plot([src.x, dest.x], [src.y, dest.y], "-", color="royalblue", marker="o", markersize=3,
                        zorder=2)
            i += 1

        if idx < 3:
            ax.set_xlim(center[0]-x, center[0]+x)
            ax.set_ylim(center[1]-y, center[1]+y)

        x = x * 1.25
        y = y * 1.25

        plt.savefig(os.path.join(cwd, "doc", "example_" + str(idx) + ".png"), dpi=150)
        plt.show()


if __name__ == '__main__':
    main()
