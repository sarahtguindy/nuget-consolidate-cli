"""
Displays all NuGet packages across projects within a solution that have incongruent versions.
"""

import os
import argparse
import concurrent.futures
import xml.etree.ElementTree as ET


def parse_csproj_file(csproj_file: str) -> dict[str, list[tuple[str, str]]]:
    """
    Parses the given .csproj file to get each package's name and version.
    """

    packages = {}
    tree = ET.parse(csproj_file)
    root = tree.getroot()

    for package_reference in root.findall(".//PackageReference"):
        package_name = package_reference.attrib["Include"]
        package_version = package_reference.attrib["Version"]
        packages[package_name] = [(os.path.basename(csproj_file), package_version)]

    return packages


def list_packages(args: argparse.Namespace) -> None:
    """
    Filters and displays all packages across projects with incongruent versions.
    """

    solution_dir = os.path.abspath(args.solution)

    csproj_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(solution_dir)
        for file in files
        if file == os.path.basename(root) + ".csproj"
    ]

    all_packages = {}

    # Collect package information for all projects
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [
            executor.submit(parse_csproj_file, csproj_file)
            for csproj_file in csproj_files
        ]

        for future in concurrent.futures.as_completed(results):
            packages = future.result()
            for package_name, package_info in packages.items():
                if package_name in all_packages:
                    all_packages[package_name].extend(package_info)
                else:
                    all_packages[package_name] = package_info

    # Filter and print consolidated package information
    for package_name, package_info in all_packages.items():
        if (
            len(set(version for _, version in package_info)) > 1
            and len(package_info) > 1
        ):
            print(f"\n{package_name}:")
            for project, version in package_info:
                print(f"{project} ({version})")
