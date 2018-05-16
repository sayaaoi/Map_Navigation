import matplotlib.pyplot as plt
import networkx as nx


def draw_route(src: int, dest: int, graph_name: str, graph):
    """
    Visualize shortest path between nodes.

    :param src: starting node number
    :param dest: ending node number
    :param graph_name: name of the map
    :param graph: graph object, could be any Graph(nx.Graph(), nx.DiGraph(), etc.)
    :return: map with highlighted shortest path
    """
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle(graph_name, fontsize=30)
    plt.ylim(-100, 1150)
    # get nodes numbers in shortest path
    path = nx.dijkstra_path(graph, src, dest, weight="distance")
    # The positions of each node are stored in a dictionary
    node_pos = nx.get_node_attributes(graph, 'pos')
    # Water edges
    edge_water = [(data[0], data[1]) for data in list(graph.edges.data('type')) if data[2] == "water"]

    # create a list of edges in the shortest path using the zip command and store it in red edges
    red_edges = list(zip(path, path[1:]))
    # if the node is in the shortest path, set it to red, else set it to white color
    node_col = ['white' if node not in path else 'red' for node in graph.nodes]
    edge_col = ['black' if edge not in red_edges else 'red' for edge in graph.edges]
    edge_width = [1 if edge not in red_edges else 4 for edge in graph.edges]
    edge_label_text = {}
    for edge in graph.edges:
        if edge in edge_water:
            edge_label_text[edge] = "water"
        else:
            edge_label_text[edge] = ""
    # draw the nodes
    nx.draw_networkx(graph, node_pos, node_color=node_col, node_size=1000, font_size=13)
    nx.draw_networkx_nodes(graph, node_pos, edgecolors='black', node_color=node_col, node_size=1000)
    # draw the edges
    nx.draw_networkx_edges(graph, node_pos, edge_color=edge_col, width=edge_width)
    # Draw the edge labels
    nx.draw_networkx_edge_labels(graph, node_pos, edge_labels=edge_label_text, font_size=8)
    # fig.set_facecolor('#96f97b')
    plt.axis("off")
    return plt.show()
