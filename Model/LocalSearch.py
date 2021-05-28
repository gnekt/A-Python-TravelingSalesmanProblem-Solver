from abc import ABC, abstractmethod
from enum import Enum

from matplotlib import pyplot as plt

from Model.Tour import Tour
import TwoOpt
from Utils.Plot import plot_local_search_line

class Neighbourhood(Enum):
    TWO_OPT = 0


class Exploration(Enum):
    FIRST_IMPROVEMENT = 0
    BEST_IMPROVEMENT = 0


class LocalSearch:

    def __init__(self, neighbourood: Neighbourhood, exploration: Exploration):
        self.neighborhood = neighbourood
        if neighbourood == Neighbourhood.TWO_OPT:
            self.neighbor = TwoOpt.move2opt
            if exploration == Exploration.FIRST_IMPROVEMENT:
                self.exploration = TwoOpt.first_improvement_evaluation
            self.evaluation = TwoOpt.delta_evaluation


    def local_search(self, tour=None, instances=None, constructive_algorithm=None, first_city=None, verbose=False):
        _length_history = {}
        _iteration = 1
        fig, scatter = plt.subplots()
        plt.ion()
        plt.show()
        if self.neighborhood == Neighbourhood.TWO_OPT:
            if constructive_algorithm:
                if not instances:
                    raise ValueError("You cannot perform a constructive algorithm without an instance of cities")
                tour = constructive_algorithm(instances, first_city, verbose=verbose)
            if not tour:
                raise ValueError("We cannot start local search without a 1st solution")
            tour.append(tour.position(0))
            tour.tour_name += " + Local Search"
            _length_history[_iteration] = tour.length()
            while True:
                try:
                    plot_local_search_line(scatter,list(_length_history.keys()),list(_length_history.values()),velocity=0.01,graph_step_by_step=False)
                    pos1, pos3 = self.exploration(tour, verbose)
                    _length_history[_iteration] = tour.length()
                    _iteration += 1
                    if pos1 is not None:
                        tour = self.neighbor(tour, pos1, pos3, verbose)
                    else:
                        tour.remove(-1)
                        return tour
                except Exception as ex:
                    print(ex)