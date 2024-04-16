"""
Lists all NuGet packages installed across projects within the given solution.
"""

import os
import argparse
import concurrent.futures
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
        packages.append(
            {
                "file": os.path.basename(csproj_file),
                "name": package_name,
                "version": package_version,
            }
        )

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

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [
            executor.submit(parse_csproj_file, csproj_file)
            for csproj_file in csproj_files
        ]

        for future in concurrent.futures.as_completed(results):
            for package in future.result():
                print(f"{package['file']}: {package['name']} ({package['version']})")
