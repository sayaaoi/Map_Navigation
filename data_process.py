import csv
import math

# modify y coordinate (run one time)
# ============================================================================
# with open('data/node_list.csv', newline="", encoding="utf-8-sig") as csvfile:
#     node_file = csv.reader(csvfile)
#     title = next(node_file)
#     with open('data/node_list_new.csv', 'w') as csv_file:
#         title_row = csv.writer(csv_file)
#         title_row.writerow(title)
#     for row in node_file:
#         row[-1] = 1000 - int(row[-1])
#         with open('data/node_list_new.csv', 'a') as csv_file:
#             new_node_file = csv.writer(csv_file)
#             new_node_file.writerow(row)
# ============================================================================

def euclidean_distance(x1: int, y1: int, x2: int, y2: int):
    return math.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))
    # return math.hypot(x1 - x2, y1 - y2)

# The following code only run once to get edge_list_new.csv
# ==========================================================================================
# # calculate edge weight based on coordinates
# with open('data/node_list_new.csv', newline="", encoding="utf-8-sig") as csvfile:
#     node_file = csv.reader(csvfile)
#     title = next(node_file)
#     coordinates = {}
#     for row in node_file:
#         coordinates[row[0]] = (row[-2], row[-1])
#
# with open('data/edge_list.csv', newline="", encoding="utf-8-sig") as f:
#     edge_file = csv.reader(f)
#     title = next(edge_file)
#     with open('data/edge_list_new.csv', 'w') as csv_file:
#         title_row = csv.writer(csv_file)
#         title_row.writerow(title)
#     title.extend(["x1", "y1", "x2", "y2", "distance"])
#     for row in edge_file:
#         row.extend([int(coordinates[row[0]][0]), int(coordinates[row[0]][1]), int(coordinates[row[1]][0]), int(coordinates[row[1]][1])])
#         distance = round(euclidean_distance(row[-4], row[-3], row[-2], row[-1]),2)
#         row.append(distance)
#         with open('data/edge_list_new.csv', 'a') as csv_file:
#             new_edge_file = csv.writer(csv_file)
#             new_edge_file.writerow([row[0], row[1], row[-1], row[3], row[4], row[5]])
# ==========================================================================================

if __name__ == "__main__":
    print(euclidean_distance(395, 390, 480, 200))
    print(euclidean_distance(480, 200, 395, 100))
    print(euclidean_distance(60, 380, 210, 310))
