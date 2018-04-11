"""
Author: Yuejun Wu
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

class Navigation:
    def __init__(self, node_file, edge_file, disable:bool):
        self._map = self.build_map(nx.DiGraph(),node_file, edge_file, disable)

    def build_map(self, graph, node_file, edge_file, disable: bool):
        node_list = pd.read_csv(node_file)
        edge_list = pd.read_csv(edge_file)
        for idx, node_attr in node_list.iterrows():
            graph.add_node(node_attr[0], attr = node_attr[1:].to_dict())
        for idx, edge_attr in edge_list.iterrows():
            if disable and edge_attr[4] == 1:
                graph.add_edge(edge_attr[0], edge_attr[1], attr=edge_attr[2:].to_dict())
            if not disable:
                graph.add_edge(edge_attr[0], edge_attr[1], attr=edge_attr[2:].to_dict())
        return graph

    def get_edge_weight(self, node1, node2):
        pass

    def set_edge_weight(self, node1, node2):
        pass

    def add_edge(self, node1, node2):
        pass

    def remove_edge(self,node1, node2):
        pass

    def add_node(self):
        pass

    def remove_node(self, index):
        pass

    def get_node_name(self, node):
        pass

    def set_node_name(self, node):
        pass

    def get_accessibility_node(self, node) ->bool:
        """
        check if a certain node/attraction is available for disabled people
        :param node:
        :return:
        """
        pass

    def attraction_open(self, current_time) ->bool:
        """
        check if a certain attraction is open at current time
        :param current_time:
        :return:
        """
        pass

    def go_through_all_nodes(self, edge_list: list) ->bool:
        """
        check if from every node can arrive at any other node in the map
        :param edge_list:
        :return:
        """
        pass

    def shortest_path(self, start, end):
        path_list = nx.shortest_path(self._map, start, end)
        return [(idx,self._map.nodes.data()[idx]['attr']['name']) for idx in path_list]

    def show_shortest_route(self, start, end):
        paths = self.shortest_path(start, end)
        for i, path in enumerate(paths):
            if i == 0:
                print("From {0}: {1}".format(path[0],path[1]))
            elif i == len(paths) - 1:
                print("Finally, you will arrive at your destination, {0}: {1}".format(path[0],path[1]))
            else:
                print("Then, take the way to {0}: {1}".format(path[0],path[1]))

    def find_nearest_bathroom(self, cur_location):
        pass

    def find_nearest_foodplace(self, cur_location):
        pass

    def draw_map(self):
        nx.draw(self._map)
        return plt.show()


if __name__ == "__main__":



## tests:
gs = Navigation("data/node_list2.csv","data/edge_list.csv", False)
# print(gs.shortest_path(10,28))
gs2 = Navigation("data/node_list2.csv","data/edge_list.csv", True)
# print(gs2.shortest_path(18,12))
# print(gs2.shortest_path(10,28))
gs.show_shortest_route(18,12)

# gs.visualization()
# gs2.visualization()

## User interface below:

