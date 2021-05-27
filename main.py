import logging

from LocalSearch import LocalSearch
from Algorithm.NearestNeighbour import nearest_neighbor_algorithm
from Algorithm.FarthestAdditionNaive import farthest_addition_algorithm_naive
from Algorithm.FarthestAddition import farthest_addition_algorithm
from Algorithm.NearestAddition import nearest_addition_algorithm
from Model.Instance import Instance,InstanceSourceType
from LocalSearch import Neighbourhood,Exploration
verbose_mode = True
if __name__ == "__main__":
    logging.basicConfig(filename="DiMaioProject.log", level=logging.INFO,filemode="w")
    logging.info("Start")
    interface = Instance(instance_type=InstanceSourceType.GoogleSheet)
    instance = interface.loader("",verbose=verbose_mode)

    logging.info("Finished")
    tour = nearest_neighbor_algorithm(instance, None, verbose=verbose_mode)
    print(tour.length())
    # tour_2 = farthest_addition_algorithm_naive(instance,None,verbose=verbose_mode,graph_velocity=0.00001,graph_step_by_step=False)
    # tour_3 = farthest_addition_algorithm(instance,None,verbose=verbose_mode,graph_velocity=0.00001,graph_step_by_step=False)
    # tour_4 = nearest_addition_algorithm(instance,None,verbose=verbose_mode,graph_velocity=0.00001,graph_step_by_step=False)
    local_search = LocalSearch(neighbourood=Neighbourhood.TWO_OPT,exploration=Exploration.FIRST_IMPROVEMENT)
    tour_ls = local_search.local_search(tour=tour,verbose=verbose_mode)
    print(tour_ls.length())
    tour.plot()
    # tour_2.tour_name="Farthest Naive"
    # tour_2.plot()
    # tour_3.tour_name = "Farthest"
    # tour_3.plot()
    # tour_4.tour_name = "Nearest Addition"
    # tour_4.plot()
    # interface.writer("Farthest Naive",tour_2)
    # print(tour.length())
    # print(tour_2.length())
    # print(tour_3.length())
    # print(tour_4.length())