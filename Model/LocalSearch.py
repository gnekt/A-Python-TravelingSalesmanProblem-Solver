from abc import ABC, abstractmethod
from enum import Enum
from Model.Tour import Tour
import TwoOpt


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
        if self.neighborhood == Neighbourhood.TWO_OPT:
            if constructive_algorithm:
                if not instances:
                    raise ValueError("You cannot perform a constructive algorithm without an instance of cities")
                tour = constructive_algorithm(instances, first_city, verbose=verbose)
            if not tour:
                raise ValueError("We cannot start local search without a 1st solution")
            tour.append(tour.position(0))
            while True:
                pos1, pos3 = self.exploration(tour, verbose)
                if pos1:
                    tour = self.neighbor(tour, pos1, pos3, verbose)
                    if verbose:
                        print(tour.length())
                else:
                    tour.remove(-1)
                    return tour

