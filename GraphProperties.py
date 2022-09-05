from Graph import Graph
from statistics import mean
from GraphUtilities import *
import matplotlib.pyplot as plt


class GraphProperties:
    def __init__(self, graph: Graph, clusters: list):
        self.graph = graph
        self.clusters = clusters
        self.number_of_clusters = len(clusters)

    def get_generated_overlapping(self):
        cluster_combinations = get_combinations(list(range(0, self.number_of_clusters)))
        number_of_connections = 0
        number_of_overlapping = 0
        for c in cluster_combinations:
            c1 = self.clusters[c[0]]
            c2 = self.clusters[c[1]]
            if len(set(c1).intersection(set(c2))) > 0:
                number_of_overlapping += 1
            for vertex in c1:
                to_break = False
                for adjacent in self.graph.adjacency_list[vertex]:
                    if adjacent in c2:
                        number_of_connections += 1
                        to_break = True
                        break
                if to_break:
                    break
        return number_of_overlapping / number_of_connections

    def get_generated_interconnectivity(self):
        # interconnectivity = (connections between clusters) / (all possible connections between clusters)
        all_possible = get_combination_two(self.number_of_clusters)
        cluster_combinations = get_combinations(list(range(0, self.number_of_clusters)))
        number_of_connections = 0
        for c in cluster_combinations:
            c1 = self.clusters[c[0]]
            c2 = self.clusters[c[1]]
            for vertex in c1:
                to_break = False
                for adjacent in self.graph.adjacency_list[vertex]:
                    if adjacent in c2:
                        number_of_connections += 1
                        to_break = True
                        break
                if to_break:
                    break
        return number_of_connections / all_possible

    def get_generated_intraconnectivity(self):
        # for each cluster, (connections between vertices in that cluster) / (all possible connections)
        all_averages = list()
        for c in self.clusters:
            all_possible = get_combination_two(len(c))
            cons_in_cluster = 0
            for vertex in c:
                cons_in_cluster += len([x for x in self.graph.adjacency_list[vertex] if vertex < x and x in c])
            all_averages.append(cons_in_cluster/all_possible)
        return mean(all_averages)

    def get_zout_per_vertex(self):
        zoutlist = list()
        for vertex in self.graph.vertices:
            vertex_degree = self.graph.vertex_degree(vertex)
            for cluster in self.clusters:
                zout = 0
                if vertex in cluster:
                    for adjacent in self.graph.adjacency_list[vertex]:
                        if adjacent not in cluster:
                            zout += 1
                    zoutlist.append(zout / vertex_degree)
        return mean(zoutlist)

    def plot_vertex_degree_histogram(self):
        degrees = list()
        for vertex in self.graph.vertices:
            degrees.append(self.graph.vertex_degree(vertex))
        plt.hist(degrees)
        plt.show()

    def get_statistics(self):
        return self.get_generated_overlapping(), self.get_generated_interconnectivity(), self.get_generated_intraconnectivity()

    def run_statistics(self):
        stats = dict()      # store all statistics here...
        average_number_of_vertices = list()
        for cluster in self.clusters:
            average_number_of_vertices.append(len(cluster))
        average_number_of_vertices = mean(average_number_of_vertices)
        stats['average number of vertices'] = average_number_of_vertices
        stats['interconnectivity'] = self.get_generated_interconnectivity()
        stats['intraconnectivity'] = self.get_generated_intraconnectivity()
        stats['overlapping'] = self.get_generated_overlapping()
        stats['zout per vertex'] = self.get_zout_per_vertex()
        stats['number of clusters']=self.clusters.__len__()
        return stats
