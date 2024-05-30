import os
import shutil

# Assign the directory to package
pack_dir = "./functions"
out_dir = "./build"

# Iterate through the folders in that directory
for name in os.listdir(pack_dir):
    # Loop through the subdirectory to create packages for each function
    for function in os.listdir(f"{pack_dir}/{name}"):
        # Check if the function has any files to pack
        if len(os.listdir(f"{pack_dir}/{name}/{function}")) == 0:
            print("Empty Function, Skipping...")
        else:
            # Create the package directory if not exists
            if not os.path.exists(f"{out_dir}/{name}"):
                os.makedirs(f"{out_dir}/{name}")

            print(f"Packaging function: {name}/{function}")
            shutil.make_archive(
                f"{out_dir}/{name}/{function}", "zip", f"{pack_dir}/{name}/{function}"
            )
