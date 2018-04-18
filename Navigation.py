"""
Author: Yuejun Wu
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import sys

class Navigation:
    def __init__(self, node_file, edge_file, disable:bool):
        """
        Constructor of Navigation. It instantiates a graph with nodes and edges

        :param node_file: node id and its attributes
        :param edge_file: nodes connect edges and edge attributes
        :param disable: whether instantiates an ADA route or not
        """
        self._map = self.build_map(nx.DiGraph(),node_file, edge_file, disable)

    def build_map(self, graph, node_file, edge_file, disable: bool):
        """
        Helper function to construct instances

        """
        node_list = pd.read_csv(node_file)
        edge_list = pd.read_csv(edge_file)
        for idx, node_attr in node_list.iterrows():
            attr = {'name': node_attr[1],
                    'disabled_accessibility':node_attr[2],
                    'open time': node_attr[3],
                    'close time': node_attr[4],
                    'average waiting time': node_attr[5],
                    'has_bathroom':node_attr[6],
                    'has_food':node_attr[7],
                    'fee':node_attr[8],
                    'type':node_attr[9],
                    'x_coord':node_attr[12],
                    'y_coord':node_attr[13]
                    }
            graph.add_node(node_attr[0], name = attr['name'], disabled_accessibility = attr['disabled_accessibility'],
                           open_time = attr['open time'], close_time = attr['close time'], avg_wait_time = attr['average waiting time'],
                           has_bathroom = attr['has_bathroom'], has_food = attr['has_food'], fee = attr['fee'], type = attr['type'],
                           x_coord = attr['x_coord'], y_coord = attr['y_coord'])
        for idx, edge_attr in edge_list.iterrows():
            attr = {'weight': edge_attr[2],
                    'type': edge_attr[3],
                    'disable_accessbility': edge_attr[4],
                    'direction': edge_attr[5]}
            if disable and edge_attr[4] == 1:
                graph.add_edge(edge_attr[0], edge_attr[1], weight = attr['weight'], type = attr['type'],
                               disable_accessbility = attr['disable_accessbility'],
                                direction = attr['direction'])
            if not disable:
                graph.add_edge(edge_attr[0], edge_attr[1], weight = attr['weight'], type = attr['type'],
                                disable_accessbility = attr['disable_accessbility'],
                                direction = attr['direction'])
        return graph

    def get_edge_weight(self, node1, node2):
        if isinstance(node1,int) and isinstance(node2, int):
            return self._map[node1][node2]['weight']

    def set_edge_weight(self, node1, node2, new_distance:float):
        if isinstance(node1, int) and isinstance(node2, int) and \
                (isinstance(new_distance, float) or isinstance(new_distance, int)):
            self._map[node1][node2]['weight'] = new_distance

    def get_node_name(self, node: int) ->str:
        if isinstance(node,int):
            return self._map.nodes.data()[node]['name']

    def set_node_name(self, node, new_name: str):
        if isinstance(new_name,str):
            self._map.nodes.data()[node]['name'] = new_name

    def get_direction(self, node1, node2) -> str:
        direction = {'N': 'north', 'S': 'south', 'W': 'west', 'E': 'east',
                  'NE': 'northeast', 'NW': 'northwest', 'SW': 'southwest', 'SE': 'southwest'}
        return direction[self._map[node1][node2]['direction']]

    def print_all_attractions(self):
        sort_attraction = {}
        for (idx, attr) in self._map.nodes.items():
            sort_attraction[idx] = attr['name']
        all_attractions = sorted(sort_attraction.items(), key = lambda x: x[1])
        for attraction in all_attractions:
            print('{:<50} {:>3}'.format(attraction[1], attraction[0]))

    def get_nodes_attributes(self, node):
        for attributes in self._map.nodes[node]:
            if attributes not in ('x_coord', 'y_coord'):
                print(attributes, ": ", self._map.nodes[node][attributes])

    def disabled_friendly_node(self, node) ->bool:
        """
        check if a certain node/attraction is available for disabled people
        :param node:
        :return:
        """
        return self._map.nodes.data()[node]['disabled_accessibility'] == 1

    def all_disabled_friendly_node(self):
        attractions = ""
        for attraction in self._map.nodes():
            if self.disabled_friendly_node(attraction):
                attractions += str(attraction) + ": "
                attractions += self.get_node_name(attraction) + "\n"
        print ("All disabled friendly attractions are: ")
        return attractions

    def attraction_open(self, current_time) ->bool:
        """
        check if a certain attraction is open at current time
        :param current_time: current time
        :return: all attractions that are still open
        """
        pass

    def go_through_all_nodes(self) ->bool:
        """
        check if from every node can arrive at any other node in the map
        :param edge_list:
        :return:
        """
        for node1 in self._map.nodes():
            for node2 in self._map.nodes():
                if not nx.has_path(self._map, node1, node2):
                    print(node1, node2)
                    return False
        return True

    def shortest_path(self, start, end, weight = 'weight'):
        path_list = nx.dijkstra_path(self._map, start, end, weight)
        return [(idx,self._map.nodes.data()[idx]['name']) for idx in path_list]

    def print_shortest_route(self, start, end):
        paths = self.shortest_path(start, end)
        for i, path in enumerate(paths):
            if i == 0:
                print("From {0}: {1}".format(path[0],path[1]))
            elif i == len(paths) - 1:
                print("Finally, you will arrive at your destination, {0}: {1}".format(path[0],path[1]))
            else:
                print("Then, take the way to {0}: {1}".format(path[0],path[1]))

    def find_nearest_bathroom(self, cur_location: int) -> tuple:
        """
        >>> gs = Navigation("data/node_list2.csv","data/edge_list3.csv", False)
        >>> print(gs.find_nearest_bathroom(9))
        (20, 'Archaeological Zones')
        """
        if self._map.nodes[cur_location]['has_bathroom'] == 1:
            return 'Your current location has a bathroom.'
        dist = sys.maxsize
        for bathroom in [idx for idx in self._map.nodes() if self._map.nodes.data()[idx]['has_bathroom'] == 1]:
            if dist > nx.dijkstra_path_length(self._map,cur_location, bathroom):
                dist = nx.dijkstra_path_length(self._map,cur_location, bathroom)
                attr_num = bathroom
        return (attr_num, self.get_node_name(attr_num))

    def find_nearest_foodplace(self, cur_location):
        if self._map.nodes[cur_location]['has_food'] == 1:
            print('Your current location has a place for food.')
        dist = sys.maxsize
        for food in [idx for idx in self._map.nodes() if self._map.nodes.data()[idx]['has_food'] == 1]:
            if dist > nx.dijkstra_path_length(self._map, cur_location, food):
                dist = nx.dijkstra_path_length(self._map, cur_location, food)
                attr_num = food
        return (attr_num, self.get_node_name(attr_num))

    def draw_map(self):
        # nx.draw(self._map)
        # return plt.show()
        pass


# if __name__ == "__main__":



## tests:
gs = Navigation("data/node_list2.csv","data/edge_list3.csv", True)
# print(gs.shortest_path(10,28))
#print(gs.get_edge_weight(19,28))
#gs.set_edge_weight(19,28, 40)
#print(gs.get_edge_weight(19,28))
#print(gs.all_disabled_friendly_node())
#gs.get_nodes_attributes(9)
#print(gs.find_nearest_bathroom(12))
#print(gs.get_edge_weight(9,20))
#gs.shortest_path(9,20)
# gs.print_all_attractions()
#print(gs.get_node_name(9))
#print(gs.all_disabled_friendly_node())
#gs2 = Navigation("data/node_list2.csv","data/edge_list.csv", True)
#print(gs.shortest_path(18,12))
print(gs.go_through_all_nodes())
# print(gs2.shortest_path(10,28))
#gs.show_shortest_route(18,12)
#print(gs.get_direction(9,20))
# gs.visualization()
# gs2.visualization()

## User interface below:

