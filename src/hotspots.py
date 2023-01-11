from newick_parser import NewickParser
import os


def main() -> None:
    cwd = ".."
    variants = [
        ("geographic.distance.matrix.csv", "airport_geographic"),
        ("effective.distance.matrix.csv", "airport_effective"),
        ("geographic.distance.matrix.country.csv", "country_geographic"),
        ("effective.distance.matrix.country.csv", "country_effective")
    ]

    for variant_matrix_name, variant_name in variants:
        variant_file_path = os.path.join(cwd, "data", f"{variant_name}.txt")
        variant_tree = None
        if os.path.exists(variant_file_path):
            with open(variant_file_path, "r") as variant_file:
                variant_newick = variant_file.readlines()[0]
                parser = NewickParser(variant_newick)
                parser.parse()
                variant_tree = parser.root
        else:
            print(f"variant file {variant_file_path} not found")

        variant_output_file_path = os.path.join(cwd, "data", f"{variant_name}.hot_spots.csv")
        with open(variant_output_file_path, "w") as variant_annotation:
            variant_annotation.writelines(variant_tree.get_hotspots())


if __name__ == '__main__':
    main()
