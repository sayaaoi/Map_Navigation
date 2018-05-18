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


def new_map():
    while True:
        node_file_name = input("Please indicate the file path of node list: ")
        node_file = Path(node_file_name)
        try:
            node_file.resolve(strict=True)
        except FileNotFoundError:
            print(red_bold + "File path doesn't exit. Please try again.\n" + endc)
            continue
        if not node_file_name[-4:] == ".csv":
            print(red_bold + "Node file must be in .csv format. Please try again. \n" + endc)
        else:
            break

    while True:
        edge_file_name = input("Please indicate the file path of edge list: ")
        edge_file = Path(edge_file_name)
        try:
            edge_file.resolve(strict=True)
        except FileNotFoundError:
            print(red_bold + "File path doesn't exit. Please try again.\n" + endc)
            continue
        if not edge_file_name[-4:] == ".csv":
            print(red_bold + "Edge file must be in .csv format. Please try again. \n" + endc)
        else:
            break
    return node_file, edge_file


def node_info(map: Map):
    """
    Useful information about the location

    """
    while True:
        try:
            which_node = eval(input("Please type in the attraction number: "))
        except NameError as err:
            print(red_col + str(err), "Please try again!" + endc)
            continue
        except SyntaxError as error:
            print(red_col + str(error) + " Please try again" + endc)
            continue
        if which_node not in map.get_map().nodes:
            print(red_col + "Wrong attraction number. Please type again." + endc)
        else:
            map.get_nodes_attributes(which_node)
            break


def node_to_node(map: Map, node_track: list, site_name: str):
    while True:
        if len(node_track) == 0:
            print("\nLet me show you the shortest path from one location to another!")
            while True:
                try:
                    src = eval(input("Please first type in the number of the starting location: \n"))
                except NameError as err:
                    print(red_col + str(err), "Please try again!" + endc)
                    continue
                except SyntaxError as error:
                    print(red_col + str(error) + " Please try again" + endc)
                    continue
                if src not in map.get_map().nodes:
                    print(red_col + "Wrong attraction number. Please type again." + endc)
                else:
                    node_track.append(src)
                    break

            while True:
                try:
                    end = eval(input("Please then type in the number of the destination location: \n"))
                except NameError as err:
                    print(red_col + str(err), "Please try again!" + endc)
                    continue
                except SyntaxError as error:
                    print(red_col + str(error) + " Please try again" + endc)
                    continue
                if end not in map.get_map().nodes:
                    print(red_col + "Wrong attraction number. Please type again." + endc)
                else:
                    node_track.append(end)
                    break
            map.print_shortest_route(src, end)
            route_viz.draw_route(src, end, site_name, map.get_map())
            break
        else:
            while True:
                try:
                    print("\nYour last location is " + map.get_node_name(node_track[-1]) +
                          "(" + str(node_track[-1]) + ")" + ".")
                    next_node = eval(input("Where do you want to go next? Please type in location number: \n"))
                except NameError as err:
                    print(red_col + str(err), "Please try again!" + endc)
                    continue
                except SyntaxError as error:
                    print(red_col + str(error) + " Please try again" + endc)
                    continue
                if next_node not in map.get_map().nodes:
                    print(red_col + "Wrong attraction number. Please type again." + endc)
                else:
                    node_track.append(next_node)
                    map.print_shortest_route(node_track[node_track.index(next_node) - 1], next_node)
                    route_viz.draw_route(node_track[node_track.index(next_node) - 1],
                                         next_node, site_name, map.get_map())
                    break
            break


def map_type(n_file, e_file, name):
    while True:
        ada = input("Would you need a handicapped-accessible route? \n1.Yes\n2.No\n")
        if ada == "1":
            map = Map(n_file, e_file, True)
            print("This is %s map. "% name)
            map.draw_map(name)
            return map
        elif ada == "2":
            map = Map(n_file, e_file, False)
            print("This is %s map. " % name)
            map.draw_map(name)
            return map
        else:
            print(red_col + "Invalid input, you must type 1 or 2" + endc)


def find_place(food_bathroom: str, map: Map):
    while True:
        try:
            cur_loc = eval(input("What's your current location's number?\n"))
        except NameError as err:
            print(err, "Please try again!")
            continue
        if cur_loc not in map.get_map().nodes:
            print(red_col + "Wrong attraction number. Please type again." + endc)
            continue
        elif food_bathroom == "bathroom":
            map.find_nearest_bathroom(cur_loc)
            break
        elif food_bathroom == "food":
            map.find_nearest_foodplace(cur_loc)
            break


def user_interface():
    new_query = True
    while True:
        if new_query is True:
            while True:
                prompt = input("Do you want to see an example of a map navigation or create one on your own?"
                               + blue_col + "\n1. Example  \n2. Create a new one \n3. Quit\n" + endc)
                if prompt == "1":
                    site_name = "Xcaret Amusement Park"
                    node_file, edge_file = "data/node_list_new.csv", "data/edge_list_new.csv"
                    break
                elif prompt == "2":
                    site_name = input("\nPlease type in the name of the place your map is designed for: \n")
                    while True:
                        node_file, edge_file = new_map()
                        try:
                            Map(node_file, edge_file, False)
                        except:
                            print(red_bold + "Files don't meet the requirement. Please check and try again!" + endc)
                            continue
                        else:
                            break
                    break
                elif prompt == "3":
                    exit()
                else:
                    print(red_col + "Invalid input, you must type 1, 2 or 3" + endc)
                    continue

            print(blue_bold + """=========================== Welcome to %s ============================
                                -------- Attraction names and ID numbers -------- \n""" % site_name + endc)

            # print all attractions alphabetically
            temp_map = Map(node_file, edge_file, False)
            print(temp_map.print_all_attractions())
            map_used = map_type(node_file, edge_file, site_name)

            node_track = []
            while True:
                msg = input("\nWhat would you like to know about " + site_name + "? "
                            + black_bold + "\n1. Route from one location to another. "
                            "\n2. Detailed information about one location"
                            "\n3. All attractions that are suitable for disabled people "
                            "\n4. Whether a given location is suitable for disabled people "
                            "\n5. All attractions that are open at a given time "
                            "\n6. The nearest bathroom "
                            "\n7. the nearest foodplace "
                            "\n8. Quit the program"
                            "\n9. Start another navigation query \n" + endc)
                if msg == "1":
                    node_to_node(map_used, node_track, site_name)
                elif msg == "2":
                    node_info(map_used)
                elif msg == "3":
                    print(map_used.all_disabled_friendly_node())
                elif msg == "4":
                    while True:
                        try:
                            node_num = eval(input("Please type in the location number: \n"))
                        except:
                            print(red_col + "Invalid input. Please try again!" + endc)
                            continue
                        if node_num not in map_used.get_map().nodes:
                            print(red_col + "Invalid location number. Please type again." + endc)
                        else:
                            print(map_used.disabled_friendly_node(node_num))
                            break
                elif msg == "5":
                    while True:
                        time = input("Please type in the time you are interested: \n")
                        try:
                            temp = map_used.attractions_open(time)
                        except:
                            print("Invalid input. Please try again!")
                            continue
                        if temp == "Sorry the range of minute is [0,60] and the range of hour is [0,12]":
                            print("Sorry the range of minute is [0,60] and the range of hour is [0,12]. Please try again!")
                        elif temp == "Sorry the time format is invalid.":
                            print("Sorry the time format is invalid. Please try again!")
                        else:
                            break
                elif msg == "6":
                    while True:
                        try:
                            cur_loc = eval(input("Please type in your current location number: \n"))
                        except:
                            print(red_col + "Invalid input. Please try again!" + endc)
                            continue
                        if cur_loc not in map_used.get_map().nodes:
                            print(red_col + "Invalid location number. Please type again." + endc)
                        else:
                            print(map_used.find_nearest_bathroom(cur_loc))
                            break
                elif msg == "7":
                    while True:
                        try:
                            cur_loc = eval(input("Please type in your current location number: \n"))
                        except:
                            print(red_col + "Invalid input. Please try again!" + endc)
                            continue
                        if cur_loc not in map_used.get_map().nodes:
                            print(red_col + "Invalid location number. Please type again." + endc)
                        else:
                            print(map_used.find_nearest_foodplace(cur_loc))
                            break
                elif msg == "8":
                    exit()
                elif msg == "9":
                    new_query = True
                    break
                else:
                    print(red_col + "Invalid input. Please try again!" + endc)
        else:
            break


if __name__ == "__main__":
    user_interface()

