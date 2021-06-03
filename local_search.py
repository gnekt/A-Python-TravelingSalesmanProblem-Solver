#############################################
# Created by Christian Di Maio, github : @christiandimaio
# v 0.1
# example: python3 local_search.py <instance_type> <instance_source_path> <verbose>
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
from Model.Instance import Instance,InstanceSourceType
from LocalSearch import NeighborhoodType,ExplorationType
from Model.Tour import Tour


if __name__ == "__main__":
    print("Local search script launched..")
    print(f"Got {len(sys.argv)-1} parameters : {sys.argv[1:]}")
    if len(sys.argv)-1 != 3:
        raise SyntaxError("You don't have the right number of parameter to proceed")

    instance_type = str(sys.argv[1])
    print(f"Instance type : {instance_type}")
    instance_source_path = str(sys.argv[2])
    print(f"Instance source : {instance_source_path}")
    verbose_mode = bool(str(sys.argv[3]).replace("'","") == "True")
    print(f"Verbose : {verbose_mode}")
    logging.basicConfig(filename="DiMaioProject.log", level=logging.INFO,filemode="w")
    logging.info("Start")
    interface = None
    if instance_type == "file":
        interface = Instance(instance_type=InstanceSourceType.File)
    if instance_type == "gsheet":
        interface = Instance(instance_type=InstanceSourceType.GoogleSheet)
    instance = interface.loader(instance_source_path, verbose=verbose_mode)
    # Initialize a tour
    tour = Tour(tour_type=instance[0].location_type,tour_name="No Constructive Algorithm")
    # Use as initiali solution directly the instance to force the local search working without any other algorithm on top
    tour.tour_cities = instance


    local_search = LocalSearch(neighbourhood=NeighborhoodType.TWO_OPT, exploration=ExplorationType.FIRST_IMPROVEMENT)
    tour = local_search.local_search(tour=tour, verbose=verbose_mode)
    tour.plot()
    interface.writer("LocalSearch", tour=tour)
    print(f"Tour lenght : {tour.length()}")