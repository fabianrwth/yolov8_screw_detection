import os


root_directory = "./dataset_mvtec/labels"


def modify_classes(file_path):
    with open(file_path, "r") as file:
        contents = file.readlines()
    with open(file_path, "w") as file:
        for line in contents:
            words = line.split()
            if words:
                try:
                    # find the first integer in the line (class number)
                    first_integer = int(words[0])

                    # initalize new first integer(new class number)
                    if first_integer in [1, 2, 3, 4, 5, 6, 8, 12, 13]:
                        new_first_integer = 0
                    if first_integer in [7, 9, 10, 11]:
                        new_first_integer = 1

                    # replace the first integer with the new value
                    new_line = line.replace(str(first_integer), str(new_first_integer), 1)
                except ValueError:
                    # the first word is not an integer, skip this line
                    new_line = line
            else:
                # empty line, skip this line
                new_line = line
            file.write(new_line)


counter = 0

for dirpath, dirnames, filenames in os.walk(root_directory):

    if dirnames == []:
        for filename in filenames:
            if filename.endswith(".txt"):
                print(filename)

                counter += 1
                print(counter)
                file_path = os.path.join(dirpath, filename)
                modify_classes(file_path)
