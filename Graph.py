from __future__ import absolute_import
from __future__ import division


class Graph:
    def __init__(self):
        self.vertices = list()
        self.adjacency_list = dict()

    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices.append(v)

    def add_vertices(self, a: list):
        for n in a:
            self.add_vertex(n)

    def add_edge(self, a, b):
        if a not in self.vertices or b not in self.vertices:
            return
        if a == b:
            return
        if a not in self.adjacency_list:
            self.adjacency_list[a] = [b]
        else:
            if b not in self.adjacency_list[a]:
                self.adjacency_list[a].append(b)
        if b not in self.adjacency_list:
            self.adjacency_list[b] = [a]
        else:
            if a not in self.adjacency_list[b]:
                self.adjacency_list[b].append(a)

    def add_edges(self, a, b: list):
        if a not in self.vertices:
            return
        else:
            for n in b:
                self.add_edge(a, n)

    def rename_vertex(self, old_vertex, new_vertex):
        if new_vertex not in self.vertices:
            self.vertices.append(new_vertex)
        if new_vertex not in self.adjacency_list:
            self.adjacency_list[new_vertex] = list()
        if old_vertex in self.vertices:
            self.vertices.remove(old_vertex)
        for vertex in self.adjacency_list[old_vertex]:
            self.adjacency_list[vertex].remove(old_vertex)

        for vertex in self.adjacency_list[old_vertex]:
            if vertex not in self.adjacency_list[new_vertex]:
                self.adjacency_list[new_vertex].append(vertex)
            if new_vertex not in self.adjacency_list[vertex]:
                self.adjacency_list[vertex].append(new_vertex)

        self.adjacency_list.pop(old_vertex)

    def get_adjacency_list(self, v):
        return self.adjacency_list[v]

    def get_cluster_neighbours(self, C):
        neighbours = []
        for n in C:
            ns = self.get_vertex_neighbors(n)
            for nx in ns:
                if nx not in neighbours:
                    neighbours.append(nx)
        return neighbours  # set(neighbours).difference(set(C))

    def get_adjacency_matrix(self):
        amatrix = list()
        for n in self.vertices:
            temp = [0 for i in range(len(self.vertices))]
            for k in self.adjacency_list[n]:
                temp[self.vertices.index(k)] = 1
            amatrix.append(temp)
        return amatrix

    def write_adjacency_matrix(self, file):
        amatrix = self.get_adjacency_matrix()
        import csv
        with open(file, 'w', newline='') as csvfile:
            sw = csv.writer(csvfile, delimiter=',')
            for r in self.get_adjacency_matrix():
                sw.writerow(r)
            

    def print_graph(self):
        for n in self.vertices:
            print(n)
            print(self.adjacency_list[n])

    def vertex_degree(self, a):
        if a not in self.vertices:
            return 0
        return len(self.adjacency_list[a])

    def get_asc_order(self):
        return sorted(self.vertices, key=lambda n: self.vertex_degree(n))

    def get_desc_order(self, ns=None):
        if ns is None:
            ns = self.vertices
        return sorted(ns, key=lambda n: self.vertex_degree(n), reverse=True)