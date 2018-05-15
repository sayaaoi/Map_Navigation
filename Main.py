from Navigation import *
from pathlib import Path


# colored console output
red_col = '\033[91m'
blue_col = '\033[94m'
blue_bold = "\033[1;34m"
red_bold = "\033[1;31m"
black_bold = "\033[1;30m"
endc = '\033[0m'


# file path validation
while True:
    prompt = input("Do you want to see an example of a map navigation or create one on your own? \n1. Example  \n2. Create a new one \n3. Quit\n")
    if prompt == "1":
        site_name = "Xcaret Amusement Park"
        node_file, edge_file = "data/node_list.csv", "data/edge_list.csv"
        break
    elif prompt == "2":
        site_name = input("What's the name of the place your map is designed for? ")
        trial_times = 0
        while True:
            node_file_name = input("Please indicate the file path of node list: ")
            trial_times += 1
            node_file = Path(node_file_name)
            try:
                node_file.resolve(strict = True)
            except FileNotFoundError:
                print("File path doesn't exit. Please try again.\n")
                continue
            if trial_times == 2:
                print("You've tried too many times.")
            elif not node_file_name[-4:] == ".csv":
                print("Node file must be in .csv format. Please try again. \n")
            else:
                break
        while True:
            edge_file_name = input("Please indicate the file path of edge list: ")
            edge_file = Path(edge_file_name)
            try:
                edge_file.resolve(strict = True)
            except FileNotFoundError:
                print("File path doesn't exit. Please try again.\n")
                continue
            if not edge_file_name[-4:] == ".csv":
                print("Edge file must be in .csv format. Please try again. \n")
            else:
                break
    elif prompt == "3":
        exit()
    else:
        print("Invalid input, you must type 1, 2 or 3")


def user_interface():
    map = Map(node_file, edge_file)

    print("""=========================== Welcome to %s ============================
                    -------- Attraction names and ID numbers -------- \n""" % site_name)
    # print all attractions alphabetically
    map.print_all_attractions()

if __name__ == "__main__":
    user_interface()

