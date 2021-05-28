from typing import List
from Model.Tour import Tour
from Model.City import City
import multiprocessing
from matplotlib import pyplot as plt

def repeated_constructive_algorithm(instances: List[City], constructive_algorithm, verbose=False) -> Tour:
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Even the graphic completition is available, due to the multi process behavior,
    # Plot all the figure it's a mess, so it is disabled here.
    # inputs = (instance,city,verbose)
    inputs = [(instances,city,False) for city in instances]

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(constructive_algorithm, inputs)

    # Pick up the one with the shortest lenght
    results.sort(key=(lambda element: element.length()))
    return results[0]


