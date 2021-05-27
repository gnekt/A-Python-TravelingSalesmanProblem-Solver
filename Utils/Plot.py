from typing import List

from Model.Tour import Tour
import matplotlib.pyplot as plt

def plot_2d_tour(tour, instances, velocity,graph_step_by_step):
    fig, ax = plt.subplots()
    x_1 = [tour_cities.get_coordinate()[1] for tour_cities in tour]
    y_1 = [tour_cities.get_coordinate()[0] for tour_cities in tour]
    ax.plot(x_1, y_1,'r-*')

    x = [city.get_coordinate()[1] for city in instances]
    y = [city.get_coordinate()[0] for city in instances]

    ax.plot(x, y, 'b*')
    ax.set(title='About as simple as it gets, folks')
    if graph_step_by_step:
        plt.show()
    else:
        plt.draw()
        plt.pause(velocity)

def plot_local_search_line(scatter,lenght_history: List[float], iteration_idx_array: List[int],velocity,graph_step_by_step):

    scatter.plot(lenght_history, iteration_idx_array, 'r-*')
    scatter.set(title='Local Search')
    if graph_step_by_step:
        plt.show()
    else:
        plt.draw()
        plt.pause(velocity)

