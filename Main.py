from Navigation import *

while (True):
    try:
        node_file = input("Please indicate the file path of node list: ")
        edge_file = input("Please indicate the file path of edge list: ")
    except FileNotFoundError:
        print("File path doesn't exit. Please type in a valid one.")
        continue
    # edge_file = input("Please indicate the file path of edge list: ")
    break

def user_interface(name: str, node_file, edge_file):
    #map = Navigation("data/node_list2.csv","data/edge_list3.csv", False)
    map = Navigation(node_file, edge_file, False)
    if name is None:
        name = input("What's the name of the place your map is designed for? ")
    print("""=========================== Welcome to %s ============================
                    -------- Attraction names and ID numbers -------- \n""" % name)
    # print all attractions alphabetically
    map.print_all_attractions()

if __name__ == "__main__":
    user_interface("Xcaret Amusement Park", node_file, edge_file)
