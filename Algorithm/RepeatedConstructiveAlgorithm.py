from typing import List
from Model.Tour import Tour
from Model.City import City
import multiprocessing

def repeated_constructive_algorithm(instances: List[City], constructive_algorithm, verbose=False) -> Tour:
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    inputs = [(instances,city,verbose) for city in instances]
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(constructive_algorithm, inputs)

    # Pick up the one with the shortest lenght
    results.sort(key=(lambda element: element.length()))
    return results[0]


