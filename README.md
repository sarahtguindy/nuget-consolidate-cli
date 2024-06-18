# NuGet Consolidate CLI

A major pain point when working with IDEs outside of Visual Studio is that there is still no feature that can replicate Visual Studio's NuGet Consolidation tab. This tool is meant to fix that.

## Prerequisites

Requires the .NET CLI to be installed (comes installed with .NET Core 3.1 SDK and later versions).

## Installation

### Option 1: Download the Executable Directly
- [Windows](https://github.com/sarahtguindy/nuget-consolidate-cli/releases/download/v1.0.0/nuget-consolidate.exe)
- [macOS]() **(coming soon)**

### Option 2: Download and Run the Installation Script

- **Windows:** [install.bat](https://github.com/sarahtguindy/nuget-consolidate-cli/releases/download/v1.0.0/install.bat)
- **macOS:** [install.sh]() **(coming soon)**

## Usage

Below are a list of the available commands and options.

```console
usage: main.py [-h] {list-packages, update-packages} ...

options:
    -h, --help                  show this help message and exit

subcommands:
    {list-packages, update-packages}
    list-packages               list installed packages
    update-packages             update packages to latest version
```

#### List Packages
```console
usage: main.py list-packages [-h] solution

positional arguments:
    solution                    path to solution file
    package                     package name

options:
    -h, --help                  show this help message and exit
    --version VERSION           update packages to specified version
```

#### Update Packages
```console
usage: main.py list-packages [-h] solution

positional arguments:
    solution                    path to solution file

options:
    -h, --help                  show this help message and exit
```