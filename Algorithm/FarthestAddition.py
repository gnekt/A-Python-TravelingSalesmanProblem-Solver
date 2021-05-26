from typing import List
from Model.Tour import Tour
from Model.City import City
import logging


def farthest_city_wrt_tour(my_tour: Tour, current_city: City, verbose: bool = False):
    """
    Check the nearest city to current city, among all the cities (instance)
    :param instance: The source list of cities
    :param current_city: The target city
    :param verbose: Verbose mode
    :return: The nearest city over the instance
    """
    logging.info(f"Nearest City: Starting looking from the source list of cities nearest to {current_city.name}")
    if verbose:
        print("\n")
        print(f"Nearest City: Starting looking from the source list of cities nearest to {current_city.name}")

    best_distance, best_city_prev, best_city_next = None, None, None
    if len(my_tour) == 1:
        best_distance = current_city.distance(my_tour[0])
        best_city_prev = my_tour[0]
        best_city_next = my_tour[0]
    else:
        for prev_city,next_city in zip(my_tour,my_tour[1:]):
            _distance_prev = current_city.distance(prev_city)
            _distance_next = current_city.distance(next_city)
            if not best_distance:
                best_distance = _distance_prev + _distance_next
                best_city_prev = prev_city
                best_city_next = next_city

            if _distance_next+_distance_next > best_distance:
                best_distance = _distance_prev + _distance_next
                best_city_prev = prev_city
                best_city_next = next_city

    # logging.info(f"Nearest City: The nearest city to {current_city.name} is {best_city.name}")
    # if verbose:
    #     print(f"Nearest City: The nearest city to {current_city.name} is {best_city.name}")
    return best_city_prev,best_city_next,best_distance

def farthest_city_finder(instance: List[City], tour: Tour, verbose: bool = False):
    _farthest_list_ = []
    idx = 0
    for city in instance:
        tour_before_city,tour_after_city,distance = farthest_city_wrt_tour(tour.tour_cities,city)
        _farthest_list_.append((tour_before_city,city,tour_after_city,distance))
    _farthest_list_.sort(key=lambda element: element[3],reverse=True)
    return _farthest_list_[0][0],_farthest_list_[0][1],_farthest_list_[0][2]

def farthest_algorithm_naive(original_instance: List[City], initial_city: City = None, verbose: bool = False):
    logging.info(f"Farthest Addition Naive: HELLO :=)")
    if verbose:
        print("\n")
        print(f"Farthest Addition Naive: HELLO :=)")
    _tour: Tour = Tour()

    # we select an initial city and remove it from the instance
    if verbose:
        print("Farthest Addition Naive: Cloning list..")
    _instance: List[City] = original_instance.copy()

    if verbose:
        print("Farthest Addition Naive: Setting up the initial instances")
    _current_city: City = _instance[-1] if not initial_city else initial_city
    _instance.remove(_current_city)
    _tour.append(_current_city)

    logging.info(f"Farthest Addition Naive: Checking the starting point")
    logging.info(f"Farthest Addition Naive: Original instance {original_instance}")
    logging.info(f"Farthest Addition Naive: Starting city {_current_city.name}")
    logging.info(f"Farthest Addition Naive: Starting Farthest Addition Naive algorithm")
    if verbose:
        print(f"Farthest Addition Naive: Start looking from the source list of cities nearest to {_current_city.name}")
        print(f"Farthest Addition Naive: Checking the starting point..")
        print(f"Farthest Addition Naive: Original instance {original_instance}")
        print(f"Farthest Addition Naive: Starting city {_current_city.name}")
        print(f"Farthest Addition Naive: Starting Farthest Addition Naive algorithm..")


    # main loop to empty the set

    iterator_idx = 1
    while _instance:
        logging.info(f"Farthest Addition Naive: Iteration {iterator_idx}, {_tour}")
        if verbose:
            print(f"Farthest Addition Naive: Iteration {iterator_idx}, {_tour}")
        prev_city,_current_city,after_city = farthest_city_finder(_instance, _tour, verbose=verbose)
        # move best city from the instance to the tour
        if prev_city == after_city:
            _tour.append(_current_city)
        else:
            _tour.add_after_city(_current_city,prev_city,verbose=verbose)
        _instance.remove(_current_city)

        logging.info(f"Farthest Addition Naive: Adding {_current_city} to the tour")
        if verbose:
            print("\n")
            print(f"Farthest Addition Naive: Adding {_current_city} to the tour")
        iterator_idx += 1

    logging.info("Farthest Addition Naive: Done.")
    logging.info(f"Farthest Addition Naive: Checking if the tour is valid..")
    if verbose:
        print(f"Farthest Addition Naive: Done.")
        print(f"Farthest Addition Naive: Checking if the tour is valid..")

    # check if it is valid
    if not _tour.is_valid(original_instance):
        logging.error(f"Farthest Addition Naive: Not valid.")
        if verbose:
            print(f"Farthest Addition Naive: Not Valid.")
        return None

    logging.info("Farthest Addition Naive: Ok.")
    logging.info(f"Farthest Addition Naive: Tour length: {_tour.length():.3f}km")
    if verbose:
        print(f"Farthest Addition Naive: Ok.")
        print(f"Farthest Addition Naive: {_tour}")
        print(f"Farthest Addition Naive: Tour length: {_tour.length():.3f}km")
    return _tour
