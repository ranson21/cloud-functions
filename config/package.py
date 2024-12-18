import os
import shutil
import argparse


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Package functions with versioning")
    parser.add_argument(
        "--version",
        help="Version number for the package. If not provided, will try to read from new_version.txt",
    )
    return parser.parse_args()


def get_version(cli_version):
    """Get version from CLI arg or file, with fallback to 'latest'"""
    if cli_version:
        return cli_version

    try:
        with open("new_version.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(
            "Warning: no version provided and new_version.txt not found, using 'latest'"
        )
        return "latest"


def create_versioned_package(version):
    # Assign the directory to package
    pack_dir = "./functions"
    out_dir = "./build"

    # Iterate through the folders in that directory
    for name in os.listdir(pack_dir):
        # Create version-specific directory
        versioned_dir = f"{out_dir}/{version}/{name}"

        # Loop through the subdirectory to create packages for each function
        for function in os.listdir(f"{pack_dir}/{name}"):
            # Check if the function has any files to pack
            function_path = f"{pack_dir}/{name}/{function}"
            if len(os.listdir(function_path)) == 0:
                print(f"Empty Function {function}, Skipping...")
                continue

            # Create the versioned package directory if not exists
            os.makedirs(versioned_dir, exist_ok=True)

            print(f"Packaging function: {name}/{function} (version: {version})")

            # Create the zip file in the versioned directory
            shutil.make_archive(f"{versioned_dir}/{function}", "zip", function_path)

            # Also create/update a copy in a 'latest' folder
            latest_dir = f"{out_dir}/latest/{name}"
            os.makedirs(latest_dir, exist_ok=True)
            shutil.copy2(
                f"{versioned_dir}/{function}.zip", f"{latest_dir}/{function}.zip"
            )


if __name__ == "__main__":
    args = parse_args()
    version = get_version(args.version)
    create_versioned_package(version)
