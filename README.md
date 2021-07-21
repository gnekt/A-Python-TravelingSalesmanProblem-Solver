# Network Optimization Project
## TSP Algorithm Developing 

This project provide different tools for searching an hamiltonian cycle (Tour) among
a set of cities which come as input for the program.\
The project provide 2 different approach for solving a TSP:

- Constructive Heuristic

    - Farthest Addition (also a Naive Version)
    - Nearest Neighbor
    - Nearest Addition
  
- Local Search
    
    - Exploration : 1st improvement
    - Neighbourhood : 2-Opt
    - Evaluation : Delta evaluation for 2-opt

The structure of the project is capable also to merge local search with 
constructive heuristic for searching a first feasible solution and then apply
a local search.

#### Other Features
- The algorithm in ```verbose mode``` shows the progress in real time of the tour
    construction.
- The data loader for the cities can manage geographical position (lat-long)
 and also euclidian position. Anyway a consistency check is applied when a new instance
  of cities is loaded.
- The program is capable of load cities from file and write a solution tour into a file, moreover
the loading/writing could be 'online' with the support of google sheet.
- The program is capable of doing multi-core processing for evaluating more than one solution at the time.
- When the cities are expressed as geographical points, the program can draw a map with the tour using Folium library.


---

Requirements:
- Python 3.8
- Install all the dependencies ``` pip install -r requirements.txt```

---

#### Utilization of the program

##### How to load a new instance?

You can choose a json/tsp file from local hard disk or using a google sheet file
assuming you can open a google developer key.

What you need for google sheet loading/writing is an ```api_key.json``` file into the root of the project.\
You can follow a tutorial on the web on how to get an api_key for gsheet.

The structure of the gsheet file follow this guideline: https://docs.google.com/spreadsheets/d/1Xy1rrvGlqaTPpoVt7X9o5Ts_Zi_UtLi447nbcO3fbGQ/edit?usp=sharing

The structure for the gsheet loader/writer follow this header:
```csv
city_name coord_1 coord_2
```
Plus a last column on the loader that could be:
- Euclidian_2D, if coord_1 is coord_x and coord_2 is coord_y as TSPLib format
- Geographical, if coord_1 is Longitude and coord_2 is Latitude

##### How to run a constructive algorithm?

Pick up the algorithm that you want to use:
```
farthest_addition.py
farthest_addition_naive.py    
nearest_neighbor.py
nearest_addition.py
```
Then you can pass to the script this parameter:
```
<repeated_version> : bool -> (True) it will iterate changing the starting city and pick the best
                             (False) starting from the last city in the instance
```
Repeated version use a multicore approach for evaluating more than one solution in parallel.
```
<apply_local_search> : bool -> (True) after computing the constructive algorithm it will apply the local search
                               (False) no local search will be applied
```
```
<instance_type> : str -> (file) : means that the instance of cities will be loaded from a file
                         (gsheet) : the instance will be loaded from google sheet at shorturl.at/hBY69
```
```
<instance_source_path> : str -> (*instance_type* is file), it will represent the absolute path of the tsp file
                                (         //     is gsheet), it will represent the name of the sheet used for loading the data
```
```
<verbose> : bool -> (True) : the script will be verbose
```

All these parameters are compulsory and they are case sensitive, so pay attention to typo.

##### I want a tour for a given cities instance applying nearest neighbor and after a local search
```
python3 nearest_neighbor.py False True file "./data sets/json/AmericanCapitals.json" True
```
---

### Some solution example can be found into the directory Result

Which try to solve The American Capitals TSP and The Djibouti TSP.

---

### Test Bench

Thanks to QuickPotato library there is also a test bench script for evaluating in terms of computational efficiency
all the approaches, the test could be done by running this command:

```commandline
python3 test_bench.py
```
It will generate an html file which represent the cpu time consuming by each part of the algorithm

---

Possible problem:
Matplotlib graph are not drawed:
```
sudo apt-get install python3-tk
```
