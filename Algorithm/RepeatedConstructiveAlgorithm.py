#############################################
# Created by Christian Di Maio, github : @christiandimaio
# v 0.1
from typing import List
from Model.Tour import Tour
from Model.City import City
import multiprocessing


def repeated_constructive_algorithm(original_instance: List[City], constructive_algorithm, verbose=False) -> Tour:
    """
        Perform the constructive algorithm changing the starting city as many time as the length of the instance
        :param original_instance: The original instance of cities
        :param constructive_algorithm: The algorithm (picked from the folder directory) will be used to construct the tour
        :param verbose: Verbose mode
        :return: A valid tour
    """
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Even the plotting is available, due to the multi-process behavior,
    # Plot all the figure it's a mess, so it is disabled here.
    # inputs = (instance,city,verbose)
    inputs = [(original_instance, city, False) for city in original_instance]

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(constructive_algorithm, inputs)

    # Pick up the one with the shortest lenght
    results.sort(key=(lambda element: element.length()))
    return results[0]
