import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import datetime
import math


class Map:
    def __init__(self, node_file, edge_file):
        """
        Constructor of a map. It instantiates a graph with nodes and edges

        :param node_file: csv file with nodes and their attributes
        :param edge_file: csv file with edges and their attributes
        """
        self._map = self._build_map(nx.DiGraph(), node_file, edge_file)

    def _build_map(self, graph, node_file, edge_file):
        """
        Helper function to construct an instance of a map

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
        if isinstance(node1, int) and isinstance(node2, int):
            return self._map[node1][node2]['distance']

    def set_edge_weight(self, node1, node2, new_distance: float):
        if isinstance(node1, int) and isinstance(node2, int) and \
                (isinstance(new_distance, float) or isinstance(new_distance, int)):
            self._map[node1][node2]['weight'] = new_distance

    def get_node_name(self, node: int) ->str:
        if isinstance(node,int):
            return self._map.nodes.data()[node]['name']

    def set_node_name(self, node, new_name: str):
        if isinstance(new_name, str):
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
            print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{:<50} {:>3}'.format(attraction[1], attraction[0]))

    def get_nodes_attributes(self, node: int):
        # show all attributes except x_cord and y_coord
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


    def format_time(self, hourstring:str):
        if len(hourstring) == 3:
            format_time = hourstring[:-2].ljust(3,'0') + hourstring[-2:]
            format_time.zfill(6)
        elif len(hourstring) == 4:
            format_time = hourstring[:-2].ljust(4,'0')+ hourstring[-2:]
        elif len(hourstring) == 5:
            format_time = hourstring.zfill(6)
        else:
            format_time = hourstring
        time_format = "%I%M%p"
        return datetime.strptime(format_time, time_format)


    def attractions_open(self, current_time):
        """
        return all attractions that are open at current time
        :param current_time: current time
        :return: all attractions that are still open
        """
        open_attraction = []
        for attraction in self._map.nodes():
            if self.format_time(current_time) >= self.format_time(self._map.nodes[attraction]['open_time']):
                open_attraction.append((attraction, self.get_node_name(attraction)))
        if len(open_attraction) == 0:
            return "Sorry, no attraction is open."
        else:
            return open_attraction


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

    def find_nearest_bathroom(self, cur_location: int):
        """
        >>> gs = Map("data/node_list.csv","data/edge_list.csv", False)
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
    gs.get_nodes_attributes(9)
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


