import argparse


def get_args():
    """
    Creates the parser to read script arguments and parses provided arguments. Optional arguments are set to their
    default value.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clean_table',
                        default=True, choices=['True', 'False'],
                        help="Clean the table before inserting logs ('True' or 'False')")
    args = parser.parse_args()

    return args


args = get_args()
