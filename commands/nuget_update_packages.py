"""
Updates all packages across projects to the latest version, or to the version specified.
"""

import os
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
    installed_packages = [pkg.get("Include") for pkg in package_references]

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

    for proj_dir in proj_dirs:
        csproj_file = os.path.join(proj_dir, os.path.basename(proj_dir) + ".csproj")

        if not is_package_installed(csproj_file, args.package):
            continue

        # Redirect standard output and standard error
        subprocess.run(
            command,
            cwd=proj_dir,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    print("Successfully updated packages.")
