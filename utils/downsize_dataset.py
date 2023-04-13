import os
import random
import shutil
import argparse

# Define the directories to select files from
root = "./dataset"
dirs = ["train", "test", "valid"]

# Define the percentage of files to select
percentage = 5


def select_files(dir1, dir2, percentage):
    # Get a list of all files in the directories
    all_files1 = os.listdir(dir1)
    all_files2 = os.listdir(dir2)

    # Check that the number of files in both directories is the same
    if len(all_files1) != len(all_files2):
        raise ValueError("Amount of files do not match")

    # Shuffle the indices of both lists randomly with replacement
    num_files_to_select = int(len(all_files1) * percentage / 100)
    indices = random.sample(range(len(all_files1)), k=num_files_to_select)
    random_indices1 = [indices[i] for i in range(num_files_to_select)]
    random_indices2 = [indices[i] for i in range(num_files_to_select)]

    # Select the files from both directories based on the shuffled indices
    selected_images = [all_files1[i] for i in random_indices1]
    selected_labels = [all_files2[i] for i in random_indices2]

    return selected_images, selected_labels


# Copy the selected files to a new directory
def copy_files(dir1, dir2, percentage, new_dir):
    # Check that both directories exist
    if not os.path.exists(dir1):
        raise ValueError(f"Directory {dir1} does not exist")
    if not os.path.exists(dir2):
        raise ValueError(f"Directory {dir2} does not exist")

    # Path of the new directory
    new_dir1 = os.path.join(new_dir, "images")
    new_dir2 = os.path.join(new_dir, "labels")

    # Select the files to be copied using the select_files function
    selected_images, selected_labels = select_files(dir1, dir2, percentage)
    print(f"Selected {len(selected_images)} images")

    # Create the new directory if it doesn't already exist
    if not os.path.exists(new_dir1) and not os.path.exists(new_dir2):
        os.makedirs(new_dir1)
        os.makedirs(new_dir2)

    # Function for overwriting files
    def remove_files_in_directory(*args):
        for directory in args:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    os.remove(os.path.join(root, file))

    # remove old data
    remove_files_in_directory(new_dir1, new_dir2)

    # Copy the selected files to the new directory
    for file in selected_images:
        src_file = os.path.join(dir1, file)
        dst_file = os.path.join(new_dir1, file)
        shutil.copy2(src_file, dst_file)

    for file in selected_labels:
        src_file = os.path.join(dir2, file)
        dst_file = os.path.join(new_dir2, file)
        shutil.copy2(src_file, dst_file)


# Apply the function to all directories (train, test, valid)
print(dirs, percentage)
for dir in dirs:

    # Define the new directory to copy the selected files to
    new_dir = os.path.join(f"dataset_downsized/{percentage}", dir)

    print(dir)
    dir1 = os.path.join(root, dir, "images")
    dir2 = os.path.join(root, dir, "labels")
    print(dir1, dir2)
    copy_files(dir1, dir2, percentage, new_dir)
