#############################################
# Created by Christian Di Maio, github : @christiandimaio
# v 0.1

from enum import Enum
from matplotlib import pyplot as plt
from Model.Tour import Tour
from Model.City import City
from typing import Callable, List
import TwoOpt
from Utils.Plot import plot_local_search_line


class Neighbourhood(Enum):
    TWO_OPT = 0


class Exploration(Enum):
    FIRST_IMPROVEMENT = 0
    BEST_IMPROVEMENT = 0


class LocalSearch:
    """
    Class for representing the local search algorithm, it has a structure that allow to generalize the three main parts
        of the algorithm:
            Neighbourhood, Exploration and Evaluation
    """
    def __init__(self, neighbourhood: Neighbourhood, exploration: Exploration):
        """
        Constructor for the class
        :param neighbourhood: The typology of the neighbourhood, only 2-opt is yet implemented
        :param exploration: The type of exploration, only 1st improvement is implemented till now
        """
        #    Assumption
        # Assuming that with python we are able to use attribute of the class as callable, we could define
        # 3 callable attributes : self.neighbor for the neighbouring, self.exploration for the exploration
        #                           self.evaluation for the evaluation
        #                           self.neighborhood = neighbourhood
        # So we can change here the behavior of this attributes without wasting time in creating useless other function
        if neighbourhood == Neighbourhood.TWO_OPT:
            # Assign to the callable attributes the 2-opt ones.
            self.neighbor = TwoOpt.move2opt
            if exploration == Exploration.FIRST_IMPROVEMENT:
                self.exploration = TwoOpt.first_improvement_evaluation
            self.evaluation = TwoOpt.delta_evaluation

    def local_search(self, tour: Tour = None, original_instance: List[City] = None,
                     constructive_algorithm: Callable = None, first_city: City = None,
                     verbose: bool = False):
        """
        Perform a local search in two ways:
            1) Given an initial tour start the searching
            2) Given an instance, we first looking for a tour with some passed constructive algorithm and then
                    apply the local search
        :param tour: (Optional) The starting tour, if it is passed *constructive_algorithm* and *original_instance* are useless
        :param original_instance: (Optional) The starting instance, if it is passed *constructive_algorithm* became compulsory
        :param constructive_algorithm: The callable constructive algorithm that we want to use for finding the first solution
        :param first_city: (Optional) Use it if you want to start from a specific City
        :param verbose: Verbose Mode
        :return: return a Tour
        """
        _length_history = {}
        _iteration = 1
        fig, scatter = plt.subplots()
        plt.ion()
        plt.show()
        if self.neighborhood == Neighbourhood.TWO_OPT:
            if constructive_algorithm:
                if not original_instance:
                    raise ValueError("You cannot perform a constructive algorithm without an instance of cities")
                tour = constructive_algorithm(original_instance, first_city, verbose=verbose)
            if not tour:
                raise ValueError("We cannot start local search without a 1st solution")
            tour.append(tour.position(0))
            tour.tour_name += " + Local Search"
            _length_history[_iteration] = tour.length()
            while True:
                try:
                    plot_local_search_line(scatter, list(_length_history.keys()), list(_length_history.values()),
                                           velocity=0.01, graph_step_by_step=False)
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
