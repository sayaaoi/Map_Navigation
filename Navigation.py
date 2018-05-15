import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import datetime
import math


class Map:
    def __init__(self, node_file, edge_file):
        """
        Given files with node data and edge data, construct a directed graph

        :param node_file: csv file with nodes and their attributes
        :param edge_file: csv file with edges and their attributes
        """
        self._map = self._build_map(nx.DiGraph(), node_file, edge_file)

    def _build_map(self, graph, node_file, edge_file):
        """
        Helper function to construct a map with nodes and edges added

        """
        # add nodes, load node attributes
        node_attrs = {}
        node_list = pd.read_csv(node_file)
        for idx, node_attr in node_list.iterrows():
            # add nodes to graph
            graph.add_node(node_attr[0])
            attr = {}
            for index in range(1,len(list(node_list.columns))):
                attr[list(node_list.columns)[index]] = node_attr[index]
            node_attrs[node_attr[0]] = attr
        # add node attributes
        nx.set_node_attributes(graph, node_attrs)

        # add edges, load edge attributes
        edge_attrs = {}
        edge_list = pd.read_csv(edge_file)
        for idx, edge_attr in edge_list.iterrows():
            graph.add_edge(edge_attr[0],edge_attr[1])
            attr = {}
            for index in range(2, len(list(edge_list.columns))):
                attr[list(edge_list.columns)[index]] = edge_attr[index]
            edge_attrs[(edge_attr[0], edge_attr[1])] = attr
        # add edge attributes
        nx.set_edge_attributes(graph, edge_attrs)
        return graph

    def get_edge_weight(self, node1, node2):
        if (node1 and node2) in self._map.nodes:
            return self._map[node1][node2]['distance']
        else:
            raise KeyError('Unexpected location number!')

    def set_edge_weight(self, node1, node2, new_distance):
        if (node1, node2) in self._map.edges & (isinstance(new_distance, float) or isinstance(new_distance, int)):
            self._map[node1][node2]['distance'] = new_distance
        else:
            raise ValueError("Unexpected input!")

    def get_node_name(self, node: int) ->str:
        if node in self._map.nodes:
            return self._map.nodes[node]['name']
        else:
            raise ValueError("Unexpected location number!")

    def set_node_name(self, node, new_name: str):
        if node in self._map.nodes and isinstance(new_name, str):
            self._map.nodes[node]['name'] = new_name
        else:
            raise ValueError("Invalid input! New name must be string, location should exist.")

    def get_direction(self, node1, node2) -> str:
        """
        Get direction of an edge
        :param node1: source node
        :param node2: destination node
        :return: direction from node1 to node2
        """
        if (node1, node2) in self._map.edges:
            direction = {'N': 'north', 'S': 'south', 'W': 'west', 'E': 'east',
                         'NE': 'northeast', 'NW': 'northwest', 'SW': 'southwest', 'SE': 'southwest'}
            return direction[self._map[node1][node2]['direction']]
        else:
            raise ValueError("Unexpected edges!")

    def print_all_attractions(self):
        """
        Display all attractions alphabetically
        :return: print formatted locations
        """
        sort_attraction = {}
        for (idx, attr) in self._map.nodes.items():
            sort_attraction[idx] = attr['name']
        all_attractions = sorted(sort_attraction.items(), key=lambda x: x[1])
        for attraction in all_attractions:
            print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{:<50} {:>3}'.format(attraction[1], attraction[0]))

    def get_nodes_attributes(self, node: int):
        # show all node attributes except x_cord and y_coord
        if node in self._map.nodes:
            for attributes in self._map.nodes[node]:
                if attributes not in ('x_coord', 'y_coord'):
                    print(attributes, ": ", self._map.nodes[node][attributes])
        else:
            raise ValueError("Unexpected location number!")

    def disabled_friendly_node(self, node: int) ->bool:
        """
        Check if a certain node/attraction is available for disabled people
        :param node: location number
        :return:
        """
        if node in self._map.nodes:
            return self._map.nodes[node]['disabled_accessibility'] == 1
        else:
            raise ValueError("Unexpected location number!")

    def all_disabled_friendly_node(self):
        """
        Display all disabled people friendly attractions
        :return:
        """
        attractions = ""
        for attraction in self._map.nodes:
            if self.disabled_friendly_node(attraction):
                attractions += str(attraction) + ": "
                attractions += self.get_node_name(attraction) + "\n"
        print("All disabled friendly attractions are: ")
        return attractions

    @staticmethod
    def format_time(timestring: str):
        # "9AM"
        if len(timestring) == 3:
            format_time = timestring[:-2].ljust(3, '0') + timestring[-2:]
            format_time.zfill(6)
        # "12PM"
        elif len(timestring) == 4:
            format_time = timestring[:-2].ljust(4, '0')+ timestring[-2:]
        # elif len(timestring) == 5:
        #     format_time = timestring.zfill(6)
        else:
            format_time = timestring
        time_format = "%I%M%p"
        return datetime.strptime(format_time, time_format)

    def attractions_open(self, time: str):
        """
        Display all attractions that are open at a specific time

        :param time: current time
        :return: all attractions that are still open
        """
        if isinstance(time, str) and time[-2:] in ("AM", "PM", "am", "pm") and time[:-2].isdigit():
            if len(time) == 4 and int(time[:2]) > 12:
                return "Sorry the time format is invalid."
            elif len(time) == 6 and (int(time[:2]) > 12 or int(time[2:4] > 60)):
                return "Sorry the range of minute is [0,60] and the range of hour is [0,12]"
            else:
                open_attraction = []
                for attraction in self._map.nodes:
                    if self.format_time(time) >= self.format_time(self._map.nodes[attraction]['open_time']):
                        open_attraction.append((attraction, self.get_node_name(attraction)))
                if len(open_attraction) == 0:
                    return "Sorry, no attraction is open."
                else:
                    return self.format_open_attractions(open_attraction)
        else:
            raise ValueError("Invalid time format!")

    def format_open_attractions(self, open_attraction: list):
        """
        Helper function to return formatted open attractions

        :param open_attraction: attractions that are open
        :return: print formatted attractions
        """
        print("These locations are open based on the time you indicate: ")
        print("{:<10} {}".format("No.", "Name"))
        sort_attraction = sorted(open_attraction, key=lambda x:x[0])
        for loc in sort_attraction:
            print("{:<10} {}".format(loc[0], loc[1]))

    def go_through_all_nodes(self) ->bool:
        """
        Check if from every node can arrive at any other node in the map

        """
        for node1 in self._map.nodes():
            for node2 in self._map.nodes():
                if not nx.has_path(self._map, node1, node2):
                    return False
        return True

    def shortest_path(self, start, end, weight='distance') ->list:
        """
        Returns the shortest weighted path from source to target in graph.
        Helper function for print_shortest_route

        :param start: start location number
        :param end: destination location number
        :param weight: distance between two locations
        :return: shortest path with location number and location name
        """
        if (start and end) in self._map.nodes:
            path_list = nx.dijkstra_path(self._map, start, end, weight)
            return [(idx,self._map.nodes[idx]['name']) for idx in path_list]
        else:
            raise ValueError("Unexpected location number!")

    def print_shortest_route(self, start: int, end: int):
        paths = self.shortest_path(start, end)
        for i, path in enumerate(paths):
            if i == 0:
                print("From {1}({0})".format(path[0], path[1]))
            else:
                direction = self.get_direction(paths[i - 1][0], path[0])
                if i == len(paths) - 1:
                    print("Finally, go {0} to your destination: {2}({1})".format(direction, path[0],path[1]))
                else:
                    print("Then, go {0} to {2}({1})".format(direction, path[0],path[1]))

    def find_nearest_bathroom(self, cur_location: int) ->str:
        """
        Display the nearest place with a bathroom.

        :param cur_location: current location number
        :return: location name and number
        """
        if cur_location in self._map.nodes:
            if self._map.nodes[cur_location]['has_bathroom'] == 1:
                return 'Your current location has a bathroom.'
            dist = sys.maxsize
            attr_num = 0
            for bathroom in [idx for idx in self._map.nodes() if self._map.nodes[idx]['has_bathroom'] == 1]:
                if dist > nx.dijkstra_path_length(self._map, cur_location, bathroom, weight="distance"):
                    dist = nx.dijkstra_path_length(self._map, cur_location, bathroom, weight="distance")
                    attr_num = bathroom
            print("The nearest location with bathroom is: ")
            return self.get_node_name(attr_num) + "(" + str(attr_num) + ")"
        else:
            raise ValueError("Unexpected location number!")

    def find_nearest_foodplace(self, cur_location) ->str:
        """
        Display the nearest place that sells food.

        :param cur_location: current location number
        :return: location name and number
        """
        if cur_location in self._map.nodes:
            if self._map.nodes[cur_location]['has_food'] == 1:
                print('Your current location has a place for food.')
            dist = sys.maxsize
            attr_num = 0
            for food in [idx for idx in self._map.nodes() if self._map.nodes[idx]['has_food'] == 1]:
                if dist > nx.dijkstra_path_length(self._map, cur_location, food):
                    dist = nx.dijkstra_path_length(self._map, cur_location, food)
                    attr_num = food
            print("The nearest location that sells food is: ")
            return self.get_node_name(attr_num) + "(" + str(attr_num) + ")"
        else:
            raise ValueError("Unexpected location number!")

    def draw_map(self, graph_name: str):
        fig = plt.figure()
        plt.title(graph_name)
        color_map = []
        for node in self._map:
            if self._map.nodes[node]['type'] == 'entertainment':
                color_map.append('brown')
            elif self._map.nodes[node]['type'] == 'culture':
                color_map.append('skyblue')
            else:
                color_map.append('green')

        weights = [(math.log(self._map[u][v]['weight']))/5 for u,v in self._map.edges()]
        nx.draw(self._map, pos=nx.get_node_attributes(self._map, 'pos'),node_size = 550, node_color = color_map,with_labels=True,
                width = weights, arrowsize = 6.5)

        # edge_labels = nx.get_edge_attributes(self._map,'type')
        # nx.draw_networkx_edge_labels(self._map,pos=nx.get_node_attributes(self._map, 'pos'),edge_labels=edge_labels, font_size=5)
        # plt.plot(self._map,'EdgeLabel',self._map.edges['type'])

        fig.set_facecolor('#b6f442')
        plt.legend()
        #plt.savefig('map1.png', facecolor=fig.get_facecolor())
        return plt.show()

    def draw_route(self, node1, node2):
        gg = self.draw_map()

if __name__ == "__main__":
    gs = Map("data/node_list.csv","data/edge_list.csv")
    #print(gs.draw_map('Xcaret Tourist Map'))
# print(gs.shortest_path(10,28))
#print(gs.get_edge_weight(19,28))
#gs.set_edge_weight(19,28, 40)
#print(gs.get_edge_weight(19,28))
#print(gs.all_disabled_friendly_node())
#gs.get_nodes_attributes(9)
#print(gs.find_nearest_bathroom(12))
    print(gs.attractions_open("6620PM"))
    #print(gs.get_edge_weight(9,20))
#gs.shortest_path(9,20)
# gs.print_all_attractions()
#print(gs.get_node_name(9))
#print(gs.all_disabled_friendly_node())
#gs2 = Navigation("data/node_list2.csv","data/edge_list.csv", True)
#print(gs.shortest_path(18,12))
#print(gs.go_through_all_nodes())
#print(gs.attractions_open('110am'))

# print(gs2.shortest_path(10,28))
#gs.show_shortest_route(18,12)
#print(gs.get_direction(9,20))
# gs.visualization()
# gs2.visualization()


