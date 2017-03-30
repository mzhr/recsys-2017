#!/usr/bin/env python3

"""
MAZHAR STUFF
"""

import argparse
from baseline import xgb

def run():
    """
    Gets Directory from commandline options and starts the xgboost baseline learning algorithm.
    """

    parser = argparse.ArgumentParser(description='')
    parser.add_argument("data_directory",
        help="""Location of User.csv, Items.csv, Interactions.csv,
                TargetItems.csv and TargetUsers.csv""")
    args = parser.parse_args()

    xgb.baseline_learn(args.data_directory)


if __name__ == "__main__":
    run()
