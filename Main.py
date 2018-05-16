from Navigation import *
import Route_Visualization as route_viz
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
        node_file, edge_file = "data/node_list_new.csv", "data/edge_list_new.csv"
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
                continue
            if not node_file_name[-4:] == ".csv":
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
    map_img = Map(node_file, edge_file, False)

    print("""=========================== Welcome to %s ============================
                    -------- Attraction names and ID numbers -------- \n""" % site_name)
    # print all attractions alphabetically
    print(map_img.print_all_attractions())
    while True:
        node_attr_q = input("Would you like to know some information about a specific attraction? \n1.Yes\n2.No\n3.Quit\n")
        if node_attr_q == "1":
            while True:
                try:
                    which_node = eval(input("Please type in the attraction number: "))
                except NameError as err:
                    print(err, "Please try again!")
                    continue
                if which_node not in map_img.get_map().nodes:
                    print("Wrong attraction number. Please type again.")
                else:
                    map_img.get_nodes_attributes(which_node)
                    while True:
                        addition = input("\nWould you like to know information about other nodes? \n1.Yes\n2.No\n")
                        if addition == "2":
                            break
                        elif addition == "1":
                            break
                    break

            break
        elif node_attr_q == "2":
            break
        elif node_attr_q == "3":
            exit()
        else:
            print("Invalid input. Please try again!")

    while True:
        ada = input("Would you a handicapped-accessible route? \n1.Yes\n2.No\n")
        if ada == "1":
            map_img = Map(node_file, edge_file, True)
            print("This is %s map. "%site_name)
            map_img.draw_map(site_name)
        elif ada == "2":
            print("This is %s map. " % site_name)
            map_img.draw_map(site_name)
            break
        else:
            print("Invalid input, you must type 1 or 2")

    while True:
        print("Let me show you the shortest path from one location to another!")
        try:
            src = eval(input("Please first type in the number of the starting location: \n"))
            end = eval(input("Please then type in the number of the destination location: \n"))
        except NameError as err:
            print(err, "Please try again!")
            continue
        if (src or end) not in map_img.get_map().nodes:
            print("Wrong attraction number. Please type again.")
        else:
            map_img.print_shortest_route(src, end)
            route_viz.draw_route(src, end, site_name, map_img.get_map())
            break

if __name__ == "__main__":
    user_interface()

