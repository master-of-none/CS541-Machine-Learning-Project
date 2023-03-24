"""
Main function to run the file.
"""

import math
import time
from networkx.algorithms.approximation import traveling_salesman_problem
from matplotlib import pyplot as plt
from run_genetic import genetic
from test_coeficients import *

from statistics import mean, variance

from utils import calculate_total_distance
from utils_genetic import plot_route, plot_improvement

# Constants such as total number of nodes and total number of tests
NUMBER_OF_NODES = 50
NUMBER_OF_TESTS = 5 # For more accuracy, change this value to a larger number like 30, 50 etc.


# Function to Perform tests
def perform_test(show_graphs=True):
    graph = generate_graph(1000, 1000, NUMBER_OF_NODES) # Generate the graph

    results = {'time': {}, 'distance': {}, 'path': {}, 'steps': {}}

    # We are implementing the Optimal Approximation algorithm
    time_start = time.time()
    results['path']['christofides'] = traveling_salesman_problem(graph, weight='distance')
    time_end = time.time()
    results['time']['christofides'] = time_end - time_start  # in seconds
    results['distance']['christofides'] = calculate_total_distance(graph, results['path']['christofides'])

    # This is the Genetic algorithm
    time_start = time.time()
    results['path']['genetic'], results['steps']['genetic'] = genetic(graph, generations=136, population_size=140,
                                                                      elite_size=28, mutation_rate=0.03)
    time_end = time.time()
    results['time']['genetic'] = time_end - time_start  # in seconds
    results['distance']['genetic'] = calculate_total_distance(graph, results['path']['genetic'])

    # This is the Ant colony optimization algorithm
    colony = AntColony(graph, 25, 40)
    time_start = time.time()
    results['path']['ants'], results['distance']['ants'], results['steps']['ants'] = colony.simulate(1.2, 1.2, 0.4, 1.5)
    time_end = time.time()
    results['time']['ants'] = time_end - time_start  # in seconds

    if show_graphs: # If we have set the variable to show the graphs graph for each test case will be presented
        create_plots(graph, results)

    return results


def create_plots(graph, results): # We will be plotting the graph
    fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(10, 5))
    plot_improvement(ax[0][0], graph, results['steps']['ants'])
    plot_route(ax[0][1], graph, results['path']['ants'])
    ax[0][0].set_title('Ant colony Optimization Algorithm')

    plot_improvement(ax[1][0], graph, results['steps']['genetic'])
    plot_route(ax[1][1], graph, results['path']['genetic'])
    ax[1][0].set_title('Genetic Algorithm')

    fig.tight_layout()
    plt.show()


def run():
    # test_coefficients_genetic(25, (100, 400), 50, (40, 120), 10, (8, 20), 2, (0, 0.04), 0.002)
    results = {'times': {'ants': [], 'genetic': []}, 'distances': {'ants': [], 'genetic': []}}

    for i in range(NUMBER_OF_TESTS):
        time_s = time.time()
        test_results = perform_test(show_graphs=True) # Set this variable to true if plots must be plotted
        time_e = time.time()

        print(f'completed {i + 1} test   Total Duration: {(time_e - time_s):.2f}')

        results['times']['ants'].append(test_results['time']['ants'])
        results['times']['genetic'].append(test_results['time']['genetic'])

        results['distances']['ants'].append(test_results['distance']['ants'])
        results['distances']['genetic'].append(test_results['distance']['genetic'])

    print('\n')

    mean_time_ants = mean(results['times']['ants'])
    mean_time_genetic = mean(results['times']['genetic'])
    mean_distance_ants = mean(results['distances']['ants'])
    mean_distance_genetic = mean(results['distances']['genetic'])

    std_time_ants = math.sqrt(variance(results['times']['ants']))
    std_time_genetic = math.sqrt(variance(results['times']['genetic']))
    std_distance_ants = math.sqrt(variance(results['distances']['ants']))
    std_distance_genetic = math.sqrt(variance(results['distances']['genetic']))

    fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(10, 5))
    ax[0][0].plot(range(1, NUMBER_OF_TESTS + 1), results['times']['ants'])
    ax[0][1].plot(range(1, NUMBER_OF_TESTS + 1), results['times']['genetic'])

    ax[1][0].plot(range(1, NUMBER_OF_TESTS + 1), results['distances']['ants'])
    ax[1][1].plot(range(1, NUMBER_OF_TESTS + 1), results['distances']['genetic'])

    ax[0][0].plot(range(1, NUMBER_OF_TESTS + 1), [mean_time_ants for _ in range(1, NUMBER_OF_TESTS + 1)])
    ax[0][1].plot(range(1, NUMBER_OF_TESTS + 1), [mean_time_genetic for _ in range(1, NUMBER_OF_TESTS + 1)])
    ax[1][0].plot(range(1, NUMBER_OF_TESTS + 1), [mean_distance_ants for _ in range(1, NUMBER_OF_TESTS + 1)])
    ax[1][1].plot(range(1, NUMBER_OF_TESTS + 1), [mean_distance_genetic for _ in range(1, NUMBER_OF_TESTS + 1)])

    ax[0][0].set_xlabel('Test number ')
    ax[0][1].set_xlabel('Test number ')
    ax[1][0].set_xlabel('Test number ')
    ax[1][1].set_xlabel('Test number ')
    ax[0][0].set_ylabel('Time [s]')
    ax[0][1].set_ylabel('Time [s]')
    ax[1][0].set_ylabel('Distance')
    ax[1][1].set_ylabel('Distance')

    ax[0][0].set_title('ACO algorithm')
    ax[0][1].set_title('Genetic algorithm')
    fig.tight_layout()
    # Plot the graph
    plt.show()

    print(f"Average Distance for ACO: {mean_distance_ants:.2f}")
    print(f"Average Time for ACO: {mean_time_ants:.2f}")
    print(f"Average Distance for genetic: {mean_distance_genetic:.2f}")
    print(f"Average Time for genetic: {mean_time_genetic:.2f}\n")

    print(f"Standard Deviation distance for ACO: {std_distance_ants:.2f}")
    print(f"Standard Deviation time for ACO: {std_time_ants:.2f}")
    print(f"Standard Deviation distance for genetic: {std_distance_genetic:.2f}")
    print(f"Standard Deviation time for genetic: {std_time_genetic:.2f}")


run()
