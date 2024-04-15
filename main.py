"""
Command-line tool to consolidate NuGet packages across projects in a solution.
"""

import argparse

from commands import list


def main() -> None:
    """
    Parses command-line arguments and calls the appropriate command.
    """

    parser = argparse.ArgumentParser(description="NuGet Package Manager CLI Tool")
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    # List Packages
    # Usage: nuget-cli list-packages path/to/solution/folder
    list_parser = subparsers.add_parser("list-packages", help="list installed packages")
    list_parser.add_argument("solution", help="path to the solution file")

    args = parser.parse_args()

    if args.command == "list-packages":
        list.list_packages(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
