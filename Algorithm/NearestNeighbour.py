from typing import List


from Model.Tour import Tour
from Model.City import City
import logging
from Utils.Plot import plot_2d_tour
from matplotlib import pyplot as plt


def nearest_city(instance: List[City], current_city: City, verbose: bool = False):
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

    best_distance, best_city = None, None
    for city in instance:
        _distance = current_city.distance(city)
        best_city = city if not best_city or _distance < best_distance else best_city
        best_distance = _distance if not best_distance or _distance < best_distance else best_distance

    logging.info(f"Nearest City: The nearest city to {current_city.name} is {best_city.name}")
    if verbose:
        print(f"Nearest City: The nearest city to {current_city.name} is {best_city.name}")
    return best_city


def nearest_neighbor_algorithm(original_instance: List[City], initial_city: City = None, verbose: bool = False,
                               scatter=None,graph_velocity=0.01, graph_step_by_step=False):
    logging.info(f"Nearest Neighbor: HELLO :=)")
    if verbose:
        print("\n")
        print(f"Nearest Neighbor: HELLO :=)")

    # We could assume that the original instance has all the same coordinates type.
    _tour: Tour = Tour(tour_type=original_instance[0].location_type,tour_name="Nearest Neighbour")

    # we select an initial city and remove it from the instance
    if verbose:
        print("Nearest Neighbor: Cloning list..")
    _instance: List[City] = original_instance.copy()

    if verbose:
        print("Nearest Neighbor: Setting up the initial instances")
    _current_city: City = _instance[-1] if not initial_city else initial_city
    _instance.remove(_current_city)
    _tour.append(_current_city)

    if verbose:
        if not graph_step_by_step:
            plt.ion()

        if not scatter:
            fig, scatter = plt.subplots()
            plt.show()

        plot_2d_tour(scatter=scatter, tour=_tour.tour_cities, instances=_instance, velocity=graph_velocity,
                     graph_step_by_step=graph_step_by_step)

    logging.info(f"Nearest Neighbor: Checking the starting point")
    logging.info(f"Nearest Neighbor: Original instance {original_instance}")
    logging.info(f"Nearest Neighbor: Starting city {_current_city.name}")
    logging.info(f"Nearest Neighbor: Starting Nearest Neighbor algorithm")
    if verbose:
        print(f"Nearest Neighbor: Start looking from the source list of cities nearest to {_current_city.name}")
        print(f"Nearest Neighbor: Checking the starting point..")
        print(f"Nearest Neighbor: Original instance {original_instance}")
        print(f"Nearest Neighbor: Starting city {_current_city.name}")
        print(f"Nearest Neighbor: Starting Nearest Neighbor algorithm..")

    # main loop to empty the set

    iterator_idx = 1
    while _instance:
        logging.info(f"Nearest Neighbor: Iteration {iterator_idx}, {_tour}")
        if verbose:
            print(f"Nearest Neighbor: Iteration {iterator_idx}, {_tour}")
        _current_city: City = nearest_city(_instance, _current_city, verbose=verbose)
        # move best city from the instance to the tour
        _tour.append(_current_city)
        _instance.remove(_current_city)

        logging.info(f"Nearest Neighbor: Adding {_current_city} to the tour")
        if verbose:
            print("\n")
            print(f"Nearest Neighbor: Adding {_current_city} to the tour")
        iterator_idx += 1
        if verbose:
            plot_2d_tour(scatter=scatter,tour=_tour.tour_cities, instances=_instance, velocity=graph_velocity, graph_step_by_step=graph_step_by_step)

    logging.info("Nearest Neighbor: Done.")
    logging.info(f"Nearest Neighbor: Checking if the tour is valid..")
    if verbose:
        print(f"Nearest Neighbor: Done.")
        print(f"Nearest Neighbor: Checking if the tour is valid..")

    # check if it is valid
    if not _tour.is_valid(original_instance):
        logging.error(f"Nearest Neighbor: Not valid.")
        if verbose:
            print(f"Nearest Neighbor: Not Valid.")
        return None

    logging.info("Nearest Neighbor: Ok.")
    logging.info(f"Nearest Neighbor: Tour length: {_tour.length():.3f}km")
    if verbose:
        plot_2d_tour(scatter=scatter, tour=_tour.tour_cities + [_tour.position(0)], instances=_instance,
                     velocity=graph_velocity,
                     graph_step_by_step=graph_step_by_step)
        print(f"Nearest Neighbor: Ok.")
        print(f"Nearest Neighbor: {_tour}")
        print(f"Nearest Neighbor: Tour length: {_tour.length():.3f}km")
    return _tour

