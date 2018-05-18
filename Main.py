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
            edge_file.resolve(strict=True)
        except FileNotFoundError:
            print("File path doesn't exit. Please try again.\n")
            continue
        if not edge_file_name[-4:] == ".csv":
            print("Edge file must be in .csv format. Please try again. \n")
        else:
            break
    return node_file, edge_file

# file path validation
while True:
    prompt = input("Do you want to see an example of a map navigation or create one on your own? \n1. Example  \n2. Create a new one \n3. Quit\n")
    if prompt == "1":
        site_name = "Xcaret Amusement Park"
        node_file, edge_file = "data/node_list_new.csv", "data/edge_list_new.csv"
        break
    elif prompt == "2":
        site_name = input("\nPlease type in the name of the place your map is designed for: \n")
        while True:
            try:
                new_map = new_map()
                Map(new_map[0], new_map[1], False)
            except:
                print("There are errors in files. Please check and try again!")
                continue
            else:
                map_img = Map(new_map[0], new_map[1], False)
                break
    elif prompt == "3":
        exit()
    else:
        print(red_col + "Invalid input, you must type 1, 2 or 3" + endc)


def node_info(map: Map):
    while True:
        node_attr_q = input("\nWould you like to know some information about a specific attraction? \n1.Yes\n2.No\n3.Quit\n")
        if node_attr_q == "1":
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
        elif node_attr_q == "2":
            break
        elif node_attr_q == "3":
            exit()
        else:
            print(red_col + "Invalid input. Please try again!" + endc)


def node_to_node(map: Map):
    while True:
        node_track = []
        print("\nLet me show you the shortest path from one location to another!")
        while True:
            try:
                src = eval(input("Please first type in the number of the starting location: \n"))
            except NameError as err:
                print(err, "Please try again!")
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
                print(err, "Please try again!")
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

        while True:
            msg = input("\nDo you want to go to the next place? \n1. Yes \n2. No, this is my destination.\n")
            if msg == "1":
                while True:
                    try:
                        next_node = eval(input("\nWhere do you want to go next?\n"))
                    except NameError as err:
                        print(red_col + str(err), "Please try again!" + endc)
                        continue
                    except SyntaxError as error:
                        print(red_col + str(error) + " Please try again" + endc)
                        continue
                    if next_node not in map.get_map().nodes:
                        print(red_col + "Wrong attraction number. Please type again." + endc)
                        continue
                    else:
                        node_track.append(next_node)
                        map.print_shortest_route(node_track[node_track.index(next_node) - 1], next_node)
                        route_viz.draw_route(end, next_node, site_name, map.get_map())
                        break
            elif msg == "2":
                break
            else:
                print(red_col + "Invalid input, you must type 1 or 2" + endc)
        break


def map_type(map: Map):
    while True:
        ada = input("Would you need a handicapped-accessible route? \n1.Yes\n2.No\n")
        if ada == "1":
            map = Map(node_file, edge_file, True)
            print("This is %s map. "% site_name)
            map.draw_map(site_name)
            break
        elif ada == "2":
            print("This is %s map. " % site_name)
            map.draw_map(site_name)
            break
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
    print(blue_bold + """=========================== Welcome to %s ============================
                    -------- Attraction names and ID numbers -------- \n""" % site_name + endc)
    # print all attractions alphabetically
    print(map_img.print_all_attractions())

    map_type(map_img)

    while True:
        msg = input("\nWhat would you like to know about? \n1. Route from one location to another. "
                    "\n2. Detailed information about one location\
                    \n3. All attractions that are suitable for disabled people "
                    "\n4. Whether a given location is suitable for disabled people \
                    \n5. All attractions that are open at a given time \n6. The nearest bathroom "
                    "\n7. the nearest foodplace \n8. Quit the program\
                    \n9. Start another navigation query")
        if msg == "1":
            node_to_node(map_img)
        elif msg == "2":
            node_info(map_img)
        elif msg == "3":
            map_img.all_disabled_friendly_node()
        elif msg == "4":
            while True:
                try:
                    node_num = eval(input("Please type in the location number: \n"))
                except:
                    print("Invalid input. Please try again!")
                    continue
                else:
                    map_img.disabled_friendly_node(node_num)
                    break
        elif msg == "5":
            time = input("Please type in the time you are interested: \n")
            map_img.attractions_open(time)
        elif msg == "6":
            while True:
                try:
                    cur_loc = eval(input("Please type in your current location number: \n"))
                except:
                    print("Invalid input. Please try again!")
                    continue
                else:
                    map_img.find_nearest_bathroom(cur_loc)
                    break
        elif msg == "7":
            while True:
                try:
                    cur_loc = eval(input("Please type in your current location number: \n"))
                except:
                    print("Invalid input. Please try again!")
                    continue
                else:
                    map_img.find_nearest_foodplace(cur_loc)
                    break
        elif msg == "8":
            exit()
        elif msg =="9":
            pass
        else:
            print("Invalid input. Please try again!")


if __name__ == "__main__":
    #user_interface()
    print(new_map())

