import splitfolders
import os

dir_path = os.path.join("./dataset_mvtec", "split")


# # Loop through all files in the directory and remove them
# for filename in os.listdir(dir_path):
#     file_path = os.path.join(dir_path, filename)
#     if os.path.isfile(file_path):

#         os.remove(file_path)

# # Split with a ratio.
# # To only split into training and validation set, set a tuple to `ratio`, i.e, `(.8, .2)`.
splitfolders.ratio(
    "dataset_mvtec", output=dir_path, seed=42, ratio=(0.8, 0.1, 0.1), group_prefix=None, move=False
)  # default values
