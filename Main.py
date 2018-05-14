from Navigation import *

# file path validation
while True:
    prompt = input("Do you want to see an example of Map class or create one on your own? \n1. Example  \n2. Create a new one \n3. Quit\n")
    if prompt == "1":
        site_name = "Xcaret Amusement Park"
        node_file, edge_file = "data/node_list.csv", "data/edge_list.csv"
        break
    elif prompt == "2":
        site_name = input("What's the name of the place your map is designed for? ")
        while True:
            try:
                node_file = input("Please indicate the file path of node list: ")
                edge_file = input("Please indicate the file path of edge list: ")
            except:
                #  FileNotFoundError
                print("File path doesn't exit. Please type in a valid one.")
                continue
    elif prompt == "3":
        exit()
    else:
        print("Invalid input, you must type 1, 2 or 3")


def user_interface():
    #map = Navigation("data/node_list.csv","data/edge_list.csv", False)
    #map = Map(node_file, edge_file, False)
    map = Map(node_file, edge_file, False)

    print("""=========================== Welcome to %s ============================
                    -------- Attraction names and ID numbers -------- \n""" % site_name)
    # print all attractions alphabetically
    map.print_all_attractions()

if __name__ == "__main__":
    user_interface()

