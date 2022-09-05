from __future__ import absolute_import
from __future__ import division
from Graph import Graph


class APAL:
    def __init__(self):
        self.graph = Graph()
        self.communities = dict()
        self.community_count = 0

    def evaluate(self, candidate_community, threshold):
        communities_to_remove = list()
        if self.fitness(candidate_community) < threshold:
            return
        selected_community = None
        temporary_max_value = 0
        for community in self.communities:
            temporary_value = len(self.communities[community].intersection(candidate_community)) / len(candidate_community.union(self.communities[community]))
            if candidate_community.issubset(self.communities[community]):
                return
            elif self.communities[community].issubset(candidate_community):
                communities_to_remove.append(community)
            elif temporary_value > threshold and temporary_value > temporary_max_value and self.fitness(candidate_community.union(self.communities[community])) >= threshold:
                temporary_max_value = temporary_value
                selected_community = community
        for community in communities_to_remove:
            self.communities.pop(community)
        if selected_community is not None:
            self.communities[selected_community] = candidate_community.union(self.communities[selected_community])
            return
        self.community_count += 1
        community_name = "comm" + str(self.community_count)
        self.communities[community_name] = candidate_community

    def fitness(self, candidate_community):
        sum_adjacent_vertices = 0
        for vertex in candidate_community:
            sum_adjacent_vertices += len(set(self.graph.get_adjacency_list(vertex)).intersection(set(candidate_community)))
        if sum_adjacent_vertices == 0:
            return -1
        community_order = len(candidate_community)
        return sum_adjacent_vertices / (community_order * (community_order - 1))

    def run_apal(self, t):
        for vertex in self.graph.vertices:
            adjacent_vertices = self.graph.get_adjacency_list(vertex)
            for adjacent_vertex in adjacent_vertices:
                set1 = set(adjacent_vertices).difference({adjacent_vertex})
                set2 = set(self.graph.get_adjacency_list(adjacent_vertex)).difference({vertex})
                community_set = set1.intersection(set2)
                if len(community_set) != 0:
                    community_set.add(vertex)
                    community_set.add(adjacent_vertex)
                    self.evaluate(community_set, t)
        return [list(x) for x in self.communities.values()]
