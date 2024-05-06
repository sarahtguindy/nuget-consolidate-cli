"""
Updates all packages across projects to the latest version, or to the version specified.
"""

import os
import sys
import argparse
import subprocess
import xml.etree.ElementTree as ET


def is_package_installed(csproj_file: str, package_name: str) -> bool:
    """
    Returns true if a package reference was found in the specified project file.
    """

    tree = ET.parse(csproj_file)
    root = tree.getroot()
    package_references = root.findall(".//PackageReference")
    installed_packages = [package.get("Include") for package in package_references]

    return package_name in installed_packages


def update_packages(args: argparse.Namespace) -> None:
    """
    Update all packages to the latest version, or to the version specified.
    """

    solution_dir = os.path.abspath(args.solution)

    proj_dirs = [
        root
        for root, _, files in os.walk(solution_dir)
        for file in files
        if file == os.path.basename(root) + ".csproj"
    ]

    command = ["dotnet", "add", "package", args.package]

    if args.version:
        command.append("--version")
        command.append(args.version)

    print("Updating packages...")

    updated_count = 0

    for proj_dir in proj_dirs:
        csproj_file = os.path.join(proj_dir, os.path.basename(proj_dir) + ".csproj")

        # Skip projects that don't already have the package installed
        if not is_package_installed(csproj_file, args.package):
            continue

        try:
            # Redirect standard output and standard error
            subprocess.run(
                command,
                cwd=proj_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            updated_count += 1

        except subprocess.CalledProcessError:
            print(f"Error updating '{args.package}' packages.")
            sys.exit(1)

    if not updated_count > 0:
        print(f"No '{args.package}' packages found in '{args.solution}'.")
        sys.exit(1)

    if args.version:
        print(
            f"Updated {updated_count} '{args.package}' packages to version '{args.version}'."
        )
    else:
        print(
            f"Updated {updated_count} '{args.package}' packages to the latest version."
        )

    sys.exit(0)
