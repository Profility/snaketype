import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="SnakeType",
        description="All snaketype command-line arguments"
    )

    parser.add_argument(
        "-a",
        "--amount",
        metavar="AMOUNT OF WORDS",
        default=25,
        type=int,
        help="Amount of words to type"
    )

    parser.add_argument(
        "-f",
        "--filename",
        metavar="FILENAME",
        default="words.txt",
        type=str,
        help="Name of the wordlist file"
    )

    return parser.parse_args()