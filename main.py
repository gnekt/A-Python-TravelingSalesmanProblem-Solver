import logging

from LocalSearch import LocalSearch
from Algorithm.NearestNeighbour import nearest_neighbor_algorithm
from Algorithm.FarthestAdditionNaive import farthest_addition_algorithm_naive
from Algorithm.FarthestAddition import farthest_addition_algorithm
from Algorithm.NearestAddition import nearest_addition_algorithm
from Model.Instance import Instance,InstanceSourceType
from LocalSearch import Neighbourhood,Exploration
from RepeatedConstructiveAlgorithm import repeated_constructive_algorithm
verbose_mode = False
if __name__ == "__main__":
    logging.basicConfig(filename="DiMaioProject.log", level=logging.INFO,filemode="w")
    logging.info("Start")
    interface = Instance(instance_type=InstanceSourceType.File)
    instance = interface.loader("",verbose=verbose_mode)

    logging.info("Finished")
    # tour = repeated_constructive_algorithm(instance,nearest_neighbor_algorithm)
    # print(tour.length())
    # local_search = LocalSearch(neighbourood=Neighbourhood.TWO_OPT,exploration=Exploration.FIRST_IMPROVEMENT)
    # new_tour = local_search.local_search(tour=tour,verbose=True)
    # print(new_tour.length())
    # # tour = repeated_constructive_algorithm(instance, farthest_addition_algorithm_naive, verbose=verbose_mode)
    # print(tour.length())
    # tour = repeated_constructive_algorithm(instance, farthest_addition_algorithm, verbose=verbose_mode)
    # print(tour.length())
    tour = nearest_addition_algorithm(instance, initial_city=instance[28], verbose=verbose_mode)
    print(tour.length())
    local_search = LocalSearch(neighbourood=Neighbourhood.TWO_OPT, exploration=Exploration.FIRST_IMPROVEMENT)
    new_tour = local_search.local_search(tour=tour, verbose=True)
    print(new_tour.length())