from Navigation import *

def user_interface():
    map = Navigation("data/node_list2.csv","data/edge_list3.csv", False)
    name = input("What's the name of the place your map is designed for? ")
    print("""=========================== Welcome to %s ============================
             -------- Please Enter the Map ID of Attractions below for navigation -------- """ % name)

if __name__ == "__main__":
    user_interface()
