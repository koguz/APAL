# APAL: Adjacency Propagation Algorithm 

This is APAL by Osman Doluca and Kaya Oğuz, implemented back in 2018-2019. 

Please cite: 
Doluca, O., & Oğuz, K. (2021). APAL: Adjacency Propagation Algorithm for overlapping community detection in biological networks. Information Sciences, 579, 574-590.
https://www.sciencedirect.com/science/article/abs/pii/S0020025521008318

APAL has been extended to work on weighted networks. See WAPAL for more information: https://github.com/koguz/WAPAL/
 
## Running APAL

APAL uses its own implementation of the Graph ADT. It is very straightforward to use this Graph class. 

```python
from Graph import *

g = Graph()
# add a vertex, the type can be anything, int, string or any other class
g.add_vertex(1) 
# or a list of vertices
g.add_vertices([1, 2, 3, 4])
# then, add an edge, say between 1 and 3
g.add_edge(1, 3)
# or a list of edges to a vertex
g.add_edges(2, [3, 4])
```
Once a graph is populated with vertices and edges, you can use it in APAL. 

To run APAL, create an APAL object, assign your graph to it. Then, run `run_apal(t)` with the threshold value `t`, between 0 and 1. 

```python
from APAL import *

apal = APAL()
apal.graph = g # the graph we have defined above
apal_clusters = apal.run_apal(0.75)
```

The overlapping communities found in Graph `g` will be in the `apal_clusters` variable. This repository also includes the `CompareClusters` class so that you can compare the result to a ground truth, if you have one. Assuming that the real clusters are in `clusters` variable, use it as follows for normalised mutual information (NMI) metric that is extended for overlapping communities as detailed in 

Andrea Lancichinetti et al 2009 New J. Phys. 11 033015, https://iopscience.iop.org/article/10.1088/1367-2630/11/3/033015

The result has a range of [0,1] where values closer to 1 are of communities that are more alike, therefore represent better results.

```python
from CompareClusters import CompareClusters as CC

cc = CC(g.vertices, clusters, apal_clusters)
apal_result = cc.nvi_overlapping()
```

## OGG - Overlapping Graph Generator

This is an implementation of OGG discussed in the APAL paper. Simply create an OGG object and provide the parameters to generate a random graph that contains communities that overlap.

```python
from OGG import *

ogg = OGG()
ogg.number_of_clusters = 10
ogg.average_cluster_size = 15
ogg.overlapping = 0.3
ogg.interconnectivity = 0.6
ogg.intraconnectivity = 0.6
ogg.generate_graph()
```
Once `ogg.generate_graph()` runs, the graph can be accessed with the variable `ogg.graph` and the clusters by the variable `ogg.clusters`.

