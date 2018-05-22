# Map Navigation

## Overview 
This program can help people know information about a large museum, zoo, or amusement park, and visualize the map of it. 
It can determine the “best” route for visitors to take through the facility, given its mapping knowledge of the facility and
where (a selection of) the attractions and the paths or hallways between them. The image above is a visualization example of 
Xcaret Amusement Park in Mexico generated by this program.

The program uses Python NetworkX library. I use it as the main data structure within my custom class. 

## Visualization

### Full map 
Once the user chooses the map type (either ADA map or non-ADA one) the user will be given an image of the map with all attractions listed along with their numbers in 
upper left side of the map. Each attraction(node) will have different color based on its type. For non-ADA map, it will also show water route(edge) in blue color. None of the ADA 
route is water. One example of non-ADA map is showed under [Demo](#demo). 

### Route map
The program will visualize the shortest path based on distance between two locations. 

Let's take the example of Xcaret Amusement Park, we want to know the path from node 17 to node 36. The first image is the path for people who don't have 
handicapped-accessible requirement. The second image is the path for people who have handicapped-accessible requirement. 

*Path for non-disabled people:* <br>

![route_map1](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/route_map1.png 'Non-ADA path') <br>


*Path for disabled people:* <br>

![route_map2](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/route_map2.png 'ADA path')


## Output
When the program runs, it will:<br>
o Let users choose to see an example of navigation or create one on their own. <br> 
o Alphabetically list all the attractions with location numbers. <br>
o Ask whether the user requires a handicapped-accessible route, and then show a full map.<br>
o Ask users whether they want to:<br>
> 1. **Know how to get to the next location(defaults to starting at the last end point)**
>   - Ask the user to enter their starting point and the next attraction number they want to visit.
>   - Then the program will calculate a shortest path and print clear turn-by-turn navigation
instructions with total distance.
>   - Visualize the route on the map 
> 2. **Know detailed information about a specific location**
> 3. **Find all attractions that are suitable for disabled people**
> 4. **Find whether a given location is suitable for disabled people**
> 5. **Find all attractions that are open at a given time**
> 6. **Find the nearest bathroom**
> 7. **Find the nearest food place** 
> 8. **Quit the program**
> 9. **Start another navigation query.**
<br>
<br>

### Demo
The following screenshots are outputs ran by this program: <br>

![output flow](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/output1.png)<br>

![full map](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/full%20map%20example.png 'Sample full map of Xcaret Amusement Park') <br>

![route map](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/output2.png)<br>

![route map](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/output3.png)<br>

![route map](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/route_map.png) <br>

![route map](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/output4.png) <br>

![route map](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/output5.png) <br>

![route map](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/output6.png)<br>

![route map](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/output7.png) <br>

![route map](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/output8.png) <br>



## Instructions on how to use the program:
Put [data](data) along with [Navigation program](Navigation.py), [Main program](Main.py) and [Route visualization program](Route_Visualization.py) under the same directory, 
and run [Main program](Main.py). Then follow the instructions in console. <br>

In order to create a map on your own, you need to provide two csv files. One is for node information, and the other is for edge information. <br>
If you only want to see the example, you can just run the program without worrying about the following requirements. 

**Requirements for node file:**
- It must be .csv file
- The first row must contain <br>

  ```
     *The following column name could vary but have to be at the first of all column names:*
     'location label' (could be any data type; it will appear on nodes in the map)
     
     *The following column names have to be in the file. The order doesn't matter:*
     'name'        
     'disabled_accessibility'
     'open_time': example format (9AM); hour:[0,12], minute:[0,59]; have to include 'AM' or 'PM'
     'close_time': same as 'open_time'
     'avg_wait_time': has to be number
     'has_bathroom': value should be 1 or 0
     'has_food': value should be 1 or 0
     'fee'	       
     'type'        
     'x_coord': has to be integer
     'y_coord': has to be integer

  ```
 **Requirements for edge file:**
 - It must be .csv file
 - The first row must contain<br>
 
   ```
   *The following column names have to be the same and have to be at the first, second and fifth of all column names (order matters):*
   'start_id'	
   'end_id'	
   'ADA'
   
   *The following column names have to be in the file. The order doesn't matter:*
   'distance': actual miles * 1000 (due to distance scale in the program)
   'type'
   'direction': must be one of 'N', 'S','W','E','SE','SW','NE','NW'

   ```


## All Sources Used:
[Legend of NetworkX graph](https://stackoverflow.com/questions/32931484/legend-for-networkx-draw-function?lq=1&utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)<br>
[Check whether a file exists](https://docs.python.org/3/library/pathlib.html)<br>
[Set node attributes](https://networkx.github.io/documentation/stable/reference/generated/networkx.classes.function.set_node_attributes.html)<br>
[Encoding issue when reading files](https://stackoverflow.com/a/49150749)<br>
[Time format in Python](https://docs.python.org/3/library/time.html)<br>
[NetworkX tutorial](http://avinashu.com/tutorial/pythontutorialnew/NetworkXBasics.html)<br>
[Named colors in Python](https://stackoverflow.com/questions/22408237/named-colors-in-matplotlib?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)<br>
[Text in pyplot](https://stackoverflow.com/questions/8482588/putting-text-in-top-left-corner-of-matplotlib-plot?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)<br>
[plt title font size](https://stackoverflow.com/questions/25036699/how-to-increase-plt-title-font-size/25037902?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)<br>
[plt legend argument](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html)<br>
[Doctest_whitespace](https://docs.python.org/3/library/doctest.html#doctest.NORMALIZE_WHITESPACE)<br>
[Link inside Markdown](https://stackoverflow.com/a/15843220)

