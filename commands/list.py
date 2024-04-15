"""
Lists all NuGet packages installed across projects within the given solution.
"""

import os
import argparse
import xml.etree.ElementTree as ET


def parse_csproj_file(csproj_file: str) -> list[dict[str, str]]:
    """
    Gets each package name and version or the given .csproj file.
    """

    packages = []
    tree = ET.parse(csproj_file)
    root = tree.getroot()

    for package_reference in root.findall(".//PackageReference"):
        package_name = package_reference.attrib["Include"]
        package_version = package_reference.attrib["Version"]
        packages.append({"name": package_name, "version": package_version})

    return packages


def list_packages(args: argparse.Namespace) -> None:
    """
    Displays the package name and version for all projects in the solution.
    """

    solution_dir = os.path.abspath(args.solution)

    csproj_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(solution_dir)
        for file in files
        if file == os.path.basename(root) + ".csproj"
    ]

    packages = []

    for csproj_file in csproj_files:
        proj_name = os.path.basename(csproj_file)
        packages = parse_csproj_file(csproj_file)

        for package in packages:
            print(f"{proj_name}: {package['name']} ({package['version']})")
