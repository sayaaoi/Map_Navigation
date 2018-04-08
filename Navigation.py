"""
IS590 PR (Spring 2018)
Assignment#7
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

    def shortest_path(self, start, end):
        path_list = nx.shortest_path(self._map, start, end)
        return [(idx,self._map.nodes.data()[idx]['attr']['name']) for idx in path_list]

    # def show_shorest_paths(self, start, end):
    #     paths = self.shortest_path(start, end)
    #     for i, path in enumerate(paths):
    #         if i == 0:
    #             print("From {0}: {1}".format(path[0],path[1]))
    #         elif i == len(paths) - 1:
    #             print("Finally, you will arrive at your destination, {0}: {1}".format(path[0],path[1]))
    #         else:
    #             print("Then, take the way to {0}: {1}".format(path[0],path[1]))

    def visualization(self):
        nx.draw(self._map)
        return plt.show()

## tests:
gs = Navigation("data/node_list2.csv","data/edge_list.csv", False)
# print(gs.shortest_path(10,28))
gs2 = Navigation("data/node_list2.csv","data/edge_list.csv", True)
#print(gs2.shortest_path(18,12))
# print(gs2.shortest_path(10,28))
gs.show_shorest_paths(10,28)

# gs.visualization()
# gs2.visualization()

## User interface below:
# G = nx.DiGraph()
# class hahah(G):
