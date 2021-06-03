#############################################
# Created by Christian Di Maio, github : @christiandimaio
# v 0.1
from typing import List
import matplotlib
from Model.Tour import Tour
import matplotlib.pyplot as plt
from Model.City import City

def plot_2d_tour(tour: Tour, velocity: float, graph_step_by_step: bool, instances: List[City] = None,
                 figure=None, scatter: matplotlib.axes.Axes = None):
    """
    Plot a 2d tour in matplotlib
    :param tour: The current to represent
    :param velocity: (Optional) The velocity of updating the plot, if *graph_step_by_step* is False
    :param graph_step_by_step: (True) Each plotting call will be blocking for the execution
    :param instances: (Optional) All the cities that are still outside the tour
    :param figure: Figure created outside the function and passed here
    :param scatter: A scatter created outside the function and passed here
    """
    if not scatter:
        figure, scatter = plt.subplots()
    scatter.clear()
    x_1 = [tour_cities.get_coordinate()[1] for tour_cities in tour]
    y_1 = [tour_cities.get_coordinate()[0] for tour_cities in tour]
    scatter.plot(x_1, y_1, 'r-*')
    if instances:
        x = [city.get_coordinate()[1] for city in instances]
        y = [city.get_coordinate()[0] for city in instances]
        scatter.plot(x, y, 'b*')
    scatter.set(title='About as simple as it gets, folks')
    if graph_step_by_step:
        plt.show()
    else:
        plt.draw()
        plt.pause(velocity)


def plot_local_search_line(scatter: matplotlib.axes.Axes, lenght_history: List[float], iteration_idx_array: List[int],
                           velocity: float, graph_step_by_step: bool):
    """
    Plot the evolution of the local search line
    :param scatter: A scatter created outside the function and passed here
    :param lenght_history: A list containing all the length stored during the local search, same len() as *iteration_idx_array*
    :param iteration_idx_array: A list containing the number of the iteration associated to a length value
    :param velocity: (Optional) The velocity of updating the plot, if *graph_step_by_step* is False
    :param graph_step_by_step: (Optional) (True) Each plotting call will be blocking for the execution
    :return:
    """
    scatter.plot(lenght_history, iteration_idx_array, 'r-*')
    scatter.set(title='Local Search')
    if graph_step_by_step:
        plt.show()
    else:
        plt.draw()
        plt.pause(velocity)
