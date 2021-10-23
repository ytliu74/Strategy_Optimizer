import os
import sys
import argparse
import pandas as pd


def find_tops(folder, top):
    list_path = os.path.join(folder, 'results')
    result_list = os.listdir(list_path)

    if not os.path.exists(f".\\{folder}\\bests"):
        os.mkdir(f".\\{folder}\\bests")

    for result in result_list:
        result_path = os.path.join(list_path, result)

        result_df = pd.read_csv(result_path)

        result_df = result_df.sort_values(
            by='annual_return', ascending=False).reset_index()
        result_df = result_df.drop(columns=['index', 'Unnamed: 0'])
        result_df.head(top).to_csv(
            f".\\{folder}\\bests\\best-{result[7:-4]}.csv")


def get_parsers():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str,
                        help='The folder containing target strategy.')

    parser.add_argument('--top', type=int, default=50,
                        help='Tops of each strategy.')

    args = parser.parse_args()
    if not args.folder:
        parser.print_help()
        sys.exit()

    return args


if __name__ == '__main__':
    args = get_parsers()

    find_tops(args.folder, args.top)
