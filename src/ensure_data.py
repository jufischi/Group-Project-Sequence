#!/usr/bin/python3

import os
import sys
from pathlib import Path
from typing import List, Tuple
import requests
import argparse

base_tree = (
    "https://github.com/hzi-bifo/Phylogeography_Paper" +
    "/blob/8f5c2728808b351462106fdb0d5c6ac48380d374/Data/pH1N1" +
    "/pH1N1_until_20093004_cds_rooted.labeled.phy",
    "base tree"
)
sampling_locations = (
    "https://github.com/hzi-bifo" +
    "/Phylogeography_Paper/blob/8f5c2728808b351462106fdb0d5c6ac48380d374" +
    "/Data/pH1N1/tipdata.txt",
    "sampling locations"
)
effective_country_distances = (
    "https://zenodo.org/api/files" +
    "/f4bf2554-ee90-424a-9c73-a08efaeef0bd" +
    "/effective.distance.matrix.country.csv",
    "effective country distances"
)
effective_airport_distances = (
    "https://zenodo.org/api/files" +
    "/f4bf2554-ee90-424a-9c73-a08efaeef0bd" +
    "/effective.distance.matrix.csv",
    "effective airport distances"
)
geographic_country_distances = (
    "https://zenodo.org/api/files" +
    "/f4bf2554-ee90-424a-9c73-a08efaeef0bd" +
    "/geographic.distance.matrix.country.csv",
    "geographic country distances"
)
geographic_airport_distances = (
    "https://zenodo.org/api/files" +
    "/f4bf2554-ee90-424a-9c73-a08efaeef0bd" +
    "/geographic.distance.matrix.csv",
    "geographic airport distances"
)


def create_parser():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)

    p.add_argument('-c', '--clean',
                   help="Clean the data directory", action=argparse.BooleanOptionalAction)

    p.add_argument('-d', '--download',
                   help="Download the data files", action=argparse.BooleanOptionalAction)

    p.add_argument('-n', '--no-op',
                   help="Only perform a dry-run of the action, don't actually do something",
                   action=argparse.BooleanOptionalAction)

    return(p.parse_args())


def ensure_file(description: str, url: str, path: str, dry_run: bool) -> None:
    print(f"checking {description}...")
    if not os.path.exists(path):
        print(f"downloading {description}...")
        if dry_run:
            return
        resp = requests.get(url)
        with open(path, "wb") as f:
            f.write(resp.content)
    else:
        print(f"{description} already exists as {path}")


def download_files(data_folder: str, file_list: List[Tuple[str, str]], dry_run: bool) -> None:
    for url, description in file_list:
        ensure_file(description, url, os.path.join(data_folder, os.path.basename(url)), dry_run)


def clean_folder(path: str, dry_run: bool) -> None:
    for item in Path(path).iterdir():
        if os.path.isdir(item):
            clean_folder(item, dry_run)
        elif os.path.basename(item) != ".gitkeep":
            print(f"deleting {item}...")
            if not dry_run:
                os.remove(item)


def main() -> None:
    parser = create_parser()
    print("the way you called it, this script will:")
    if parser.clean:
        print("- clean the data folder")
    if parser.download:
        print("- download data")
    if parser.no_op:
        print("- but only as a dry-run")
    if not parser.clean and not parser.download:
        print("- do nothing, you need to specify an action")
        print("use the --help parameter for details")
        sys.exit(1)

    print()
    repo_root = os.getcwd()
    data_folder = os.path.abspath(os.path.join(repo_root, "..", "data"))
    if not os.path.exists(data_folder):
        print(f"data folder {data_folder} does not exist")
        sys.exit(1)

    print(f"data folder is assumed to be {data_folder}")
    if parser.clean:
        print("deleting data...")
        clean_folder(data_folder, parser.no_op)
        print("done")
        print()
    if parser.download:
        print("downloading data...")
        download_files(data_folder, [
            base_tree,
            sampling_locations,
            effective_airport_distances,
            effective_country_distances,
            geographic_country_distances,
            geographic_airport_distances
            ], parser.no_op)
        print("done")


if __name__ == "__main__":
    main()
