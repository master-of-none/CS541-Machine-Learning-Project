import copy
import numpy as np


class Ant:
    NODES_NOT_AVAILABLE = -1

    def __init__(self, id, graph, start_node):
        self.id = id
        self.graph = graph
        self.path = [start_node]
        self.start_node = start_node
        self.current_node = start_node
        self.cost = 0

    # available_nodes is obtained from get_available_nodes in the calling function
    def count_probability(self, available_nodes, pheromone_exponent, length_exponent):
        probabilities = {}
        probability_numerator = {}
        probability_denominator = 0

        for node in available_nodes:
            pheromone = self.graph[self.current_node][node]['pheromone']
            length_coefficient = 1 / self.graph[self.current_node][node]['distance']

            probability_numerator[node] = (pheromone ** pheromone_exponent) * (length_coefficient ** length_exponent)
            probability_denominator += probability_numerator[node]

        for node in available_nodes:
            probabilities[node] = probability_numerator[node] / probability_denominator

        return probabilities

    def get_available_nodes(self):
        available_nodes = list(copy.deepcopy(self.graph.nodes))

        for node in self.path:
            available_nodes.remove(node)

        return available_nodes

    def move_to(self, node):
        self.path.append(node)
        self.cost += self.graph[self.current_node][node]['distance']
        self.current_node = node

    def leave_pheromones(self, pheromone_coefficient):
        pheromone_value = self.calculate_pheromone(pheromone_coefficient)
        for i in range(len(self.path) - 1):
            self.graph[self.path[i]][self.path[i+1]]['pheromone'] += pheromone_value

    def calculate_pheromone(self, pheromone_coefficient):
        return pheromone_coefficient / self.cost

    # returns node index; if no nodes are available then it returns NODES_NOT_AVAILABLE
    def select_move(self, pheromone_exponent, length_exponent):
        available_nodes = self.get_available_nodes()
        if not available_nodes:
            return self.NODES_NOT_AVAILABLE

        probabilities = self.count_probability(available_nodes, pheromone_exponent, length_exponent)

        return np.random.choice(available_nodes, p=list(probabilities.values()))

    def go(self, pheromone_exponent, length_exponent):
        selected_node = self.select_move(pheromone_exponent, length_exponent)
        while selected_node != self.NODES_NOT_AVAILABLE:
            self.move_to(selected_node)
            selected_node = self.select_move(pheromone_exponent, length_exponent)

        self.move_to(self.start_node)

        return self.cost
