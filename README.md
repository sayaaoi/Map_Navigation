# Map Navigation
![full map](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/full%20map%20example.png 'Sample full map of Xcaret Amusement Park')

## Overview 
This program can help people digitize and visualize the map of a large museum, zoo, or amusement park. 
It can determine the “best” route for visitors to take through the facility, given its mapping knowledge of the facility and
where (a selection of) the attractions and the paths or hallways between them. 

The program uses Python NetworkX library. I use it as the main data structure within my custom class.

## Output
When the program runs, it will:<br>
>o Alphabetically list all the attractions it knows about with ID numbers. <br>
o Ask the user to enter their starting point and the next attraction they want to visit.<br>
o Ask whether the user requires a handicapped-accessible route.<br>
o Then it will calculate a shortest path and print clear turn-by-turn navigation
instructions with total distance.<br>
o Then it should allow the user to quit or enter another navigation query, which defaults
to starting at the last end point.

### Visualization
#### Full map 

#### Route map
For example, we want to know the path from node 17 to node 36. The first image is the path for people who don't need 
handicapped-accessible requirement. The second image is the path for people have handicapped-accessible requirement. 

![route_map1](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/route_map1.png 'Non-ADA path') 

![route_map2](https://github.com/sayaaoi/Map_Navigation/blob/master/Sample/route_map2.png 'ADA path')


## Instructions on how to use the program:


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

