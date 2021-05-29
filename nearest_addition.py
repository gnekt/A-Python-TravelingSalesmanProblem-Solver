#############################################
# Created by Christian Di Maio, github : @christiandimaio
# v 0.1
# example: python3 nearest_addition.py <repeated_version> <apply_local_search> <instance_type> <instance_source_path> <verbose>
# <repeated_version> : bool -> (True) it will iterate changing the starting city and pick the best
#                               (False) starting from the last city in the instance
# <apply_local_search> : bool -> (True) after computing the constructive algorithm it will apply the local search
#                                (False) no local search will be applied
# <instance_type> : str -> (file) : means that the instance of cities will be loaded from a file
#                          (gsheet) : the instance will be loaded from google sheet
# <instance_source_path> : str -> (*instance_type* is file), it will represent the absolute path of the tsp file
#                                 (         //     is gsheet), it will represent the name of the sheet used for loading the data
# <verbose> : bool -> (True) : the script will be verbose

import sys
import logging
sys.path.append("./Algorithm")
sys.path.append("./Model")
sys.path.append("./Utils")
from LocalSearch import LocalSearch
from ConstructiveHeuristic.NearestAddition import nearest_addition_algorithm
from Model.Instance import Instance,InstanceSourceType
from LocalSearch import NeighbourhoodType,ExplorationType
from ConstructiveHeuristic.RepeatedConstructiveAlgorithm import repeated_constructive_algorithm
verbose_mode = False

if __name__ == "__main__":
    print("Nearest addition naive script launched..")
    print(f"Got {len(sys.argv)-1} parameters : {sys.argv[1:]}")

    if len(sys.argv)-1 != 5:
        raise SyntaxError("You don't have the right number of parameter to proceed")

    repeated_version = bool(str(sys.argv[1]).replace("'","") == "True")
    print(f"Repeated versione : {repeated_version}")
    apply_local_search = bool(str(sys.argv[2]).replace("'","") == "True")
    print(f"Local search enabled : {apply_local_search}")
    instance_type = str(sys.argv[3])
    print(f"Instance type : {instance_type}")
    instance_source_path = str(sys.argv[4])
    print(f"Instance source : {instance_source_path}")
    verbose_mode = bool(str(sys.argv[5]).replace("'","") == "True")
    print(f"Verbose : {verbose_mode}")
    logging.basicConfig(filename="DiMaioProject.log", level=logging.INFO,filemode="w")
    logging.info("Start")
    interface = None
    if instance_type == "file":
        interface = Instance(instance_type=InstanceSourceType.File)
    if instance_type == "gsheet":
        interface = Instance(instance_type=InstanceSourceType.GoogleSheet)
    instance = interface.loader(instance_source_path, verbose=verbose_mode)
    tour = None

    if apply_local_search:
        local_search = LocalSearch(neighbourhood=NeighbourhoodType.TWO_OPT, exploration=ExplorationType.FIRST_IMPROVEMENT)
    if repeated_version:
        tour = repeated_constructive_algorithm(original_instance=instance,constructive_algorithm=nearest_addition_algorithm,verbose=verbose_mode)
        if apply_local_search:
            tour = local_search.local_search(tour=tour,verbose=verbose_mode)
    else:
        if apply_local_search:
            tour = local_search.local_search(original_instance=instance,constructive_algorithm=nearest_addition_algorithm,
                                                  verbose=verbose_mode)
        else:
            tour = nearest_addition_algorithm(original_instance=instance,verbose=verbose_mode)
    tour.plot()
    print(f"Tour lenght : {tour.length()}")