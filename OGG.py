from Graph import Graph
from random import randrange, seed, uniform, sample
from GraphUtilities import *


class OGG:  # Overlapping Graph Generator
    def __init__(self):
        self.graph = Graph()
        self.seed = -1                  # leave it as -1 for random seed
        self.number_of_clusters = 10    # number of clusters
        self.average_cluster_size = 10  # average cluster size
        self.interconnectivity = 0.5    # between clusters
        self.intraconnectivity = 0.9    # within clusters
        self.overlapping = 0.3          # ratio of overlapping vertices in interconnecting clusters
        self.connect_ratio = 0.15       # what ratio of vertices should be used in overlapping / connecting clusters...
        self.verbose = False            # by default, don't print any messages
        self.clusters = list()          # clusters - we will need them when we are measuring the results using Hamming.

    def generate_graph(self):
        # TODO: Check parameters if they are appropriate
        if self.seed > 0:
            seed(self.seed)

        # the following block determines the number of vertices in every cluster, and their cluster's intraconnectivity
        nv = list()                                 # number of vertices in each cluster
        ia = list()                                 # intraconnectivity of each cluster
        fa = self.intraconnectivity * 2 - 1
        for i in range(0, self.number_of_clusters):
            # the average for this list is close to self.average_cluster_size, the smallest should be 3 nodes...
            nv.append(randrange(3, self.average_cluster_size * 2 - 3))
            ia.append(uniform(fa, 1))

        # the following block connects the clusters
        cluster_ids = list(range(0, self.number_of_clusters))
        connected_cluster_set = get_connected_vertices(cluster_ids, self.interconnectivity)
        unconnected_cluster_set = set(get_combinations(cluster_ids)).difference(connected_cluster_set)

        # now, we need to count the degree of clusters (as in vertices)
        cluster_degrees = [0 for a in cluster_ids]
        for connection in connected_cluster_set:
            cluster_degrees[connection[0]] += 1
            cluster_degrees[connection[1]] += 1

        # this ensures that we have enough vertices in the cluster to connect clusters...
        # itsy bitsy details...
        number_of_nodes_to_share = list()
        for cluster in cluster_ids:
            # for each connection, there has to be (number of nodes) * connect_ratio nodes, so:
            each_cluster = round(nv[cluster] * self.connect_ratio)
            if each_cluster < 1:
                each_cluster = 1    # make sure there is at least one node for each cluster connection
            number_of_nodes_to_share.append(each_cluster * cluster_degrees[cluster])
            if nv[cluster] < cluster_degrees[cluster] * each_cluster:
                nv[cluster] = cluster_degrees[cluster] * each_cluster + 1  # accommodate more nodes...

        nc = 1
        rs = 1
        while nc <= self.number_of_clusters:
            # create vertices with appropriate integer names...
            vertices = list(range(rs, rs+nv[nc-1]))
            self.graph.add_vertices(vertices)
            # the cluster is connected with the least number of edges and the edges are returned...
            connected_vertex_set = get_connected_vertices(vertices, ia[nc-1])
            # add the sampled connections to the graph
            for c in connected_vertex_set:
                self.graph.add_edge(c[0], c[1])
            # save the cluster vertices.
            self.clusters.append(vertices)
            rs = rs + nv[nc-1]
            nc = nc + 1
        if self.verbose:
            print(self.clusters)

        # Merging clusters
        # step 1: select nodes to share... randomly...
        nodes_to_share = list()
        for cid, cluster in enumerate(self.clusters):
            nodes_to_share.append(sample(cluster, number_of_nodes_to_share[cid]))

        # step 2: sample connections for overlapping and edge-connection sets
        overlapping_set = sample(connected_cluster_set, round(len(connected_cluster_set) * self.overlapping))
        connect_with_edge_set = list(set(connected_cluster_set).difference(set(overlapping_set)))
        for connection in connect_with_edge_set:
            c1 = connection[0]
            c2 = connection[1]
            ns = min(number_of_nodes_to_share[c1] // cluster_degrees[c1], number_of_nodes_to_share[c2] // cluster_degrees[c2])
            for ii in range(ns):
                n1 = nodes_to_share[c1].pop()
                n2 = nodes_to_share[c2].pop()
                # add an edge between these two nodes
                self.graph.add_edge(n1, n2)

        for connection in overlapping_set:
            c1 = connection[0]
            c2 = connection[1]
            ns = min(number_of_nodes_to_share[c1] // cluster_degrees[c1], number_of_nodes_to_share[c2] // cluster_degrees[c2])
            for ii in range(ns):
                n1 = nodes_to_share[c1].pop()
                n2 = nodes_to_share[c2].pop()
                # rename n2 to n1...
                self.graph.rename_vertex(n2, n1)
                for cluster in self.clusters:
                    if n2 in cluster:
                        cluster.remove(n2)
                        cluster.append(n1)

        for connection in unconnected_cluster_set:
            # there shouldn't be any connections between these clusters... however, overlapping can create such
            # connections. let's find them :)
            c1 = self.clusters[connection[0]]
            c2 = self.clusters[connection[1]]
            for vertex in c1:
                vertices_to_remove = list()
                for adjacent in self.graph.adjacency_list[vertex]:
                    if adjacent in c2:
                        vertices_to_remove.append(adjacent)
                for adjacent in vertices_to_remove:
                    self.graph.adjacency_list[vertex].remove(adjacent)
                    self.graph.adjacency_list[adjacent].remove(vertex)

        unique_clusters = list()
        for cluster in self.clusters:
            temporary_cluster = list()
            for vertex in cluster:
                if vertex not in temporary_cluster:
                    temporary_cluster.append(vertex)
            unique_clusters.append(temporary_cluster)
        self.clusters = unique_clusters

