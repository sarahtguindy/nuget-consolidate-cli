"""
Command-line tool to consolidate NuGet packages across projects in a solution.
"""

import argparse

from commands import nuget_list_packages, nuget_update_packages


def main() -> None:
    """
    Parses command-line arguments and calls the appropriate command.
    """

    parser = argparse.ArgumentParser(description="NuGet Package Manager CLI Tool")
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    # List packages
    # Usage: nuget-cli list-packages solution
    list_parser = subparsers.add_parser("list-packages", help="list installed packages")
    list_parser.add_argument("solution", help="path to the solution file")

    # Update packages
    # Usage: nuget-cli update-packages solution package-name --version x.y.z
    update_parser = subparsers.add_parser(
        "update-packages", help="update packages to latest version"
    )
    update_parser.add_argument("solution", help="path to the solution file")
    update_parser.add_argument("package", help="package name")
    update_parser.add_argument("--version", help="update packages to specified version")

    args = parser.parse_args()

    if args.command == "list-packages":
        nuget_list_packages.list_packages(args)
    elif args.command == "update-packages":
        nuget_update_packages.update_packages(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
