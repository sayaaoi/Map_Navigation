from Navigation import *
from pathlib import Path

# file path validation
while True:
    prompt = input("Do you want to see an example of a map navigation or create one on your own? \n1. Example  \n2. Create a new one \n3. Quit\n")
    if prompt == "1":
        site_name = "Xcaret Amusement Park"
        node_file, edge_file = "data/node_list.csv", "data/edge_list.csv"
        break
    elif prompt == "2":
        site_name = input("What's the name of the place your map is designed for? ")
        while True:
            node_file_name = input("Please indicate the file path of node list: ")
            node_file = Path(node_file_name)
            try:
                node_file.resolve(strict = True)
            except FileNotFoundError:
                print("File path doesn't exit. Please try again.\n")
            else:
                break
        while True:
            edge_file_name = input("Please indicate the file path of edge list: ")
            edge_file = Path(edge_file_name)
            try:
                edge_file.resolve(strict = True)
            except FileNotFoundError:
                print("File path doesn't exit. Please try again.\n")
            else:
                break
    elif prompt == "3":
        exit()
    else:
        print("Invalid input, you must type 1, 2 or 3")


def user_interface():
    map = Map(node_file, edge_file, False)

    print("""=========================== Welcome to %s ============================
                    -------- Attraction names and ID numbers -------- \n""" % site_name)
    # print all attractions alphabetically
    map.print_all_attractions()

if __name__ == "__main__":
    user_interface()

