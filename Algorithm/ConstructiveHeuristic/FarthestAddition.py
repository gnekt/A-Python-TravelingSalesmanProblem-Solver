#############################################
# Created by Christian Di Maio, github : @christiandimaio
# v 0.1
from typing import List
import matplotlib
from matplotlib import pyplot as plt
from Model.Tour import Tour
from Model.City import City
import logging
from Utils.Plot import plot_2d_tour


def nearest_city_wrt_tour(my_tour: List[City], current_city: City, verbose: bool = False) -> (City, City, float):
    """
    Given a city, evaluate the two adjacent city on the tour that are nearest to the given one
    :param my_tour: The current tour
    :param current_city: The target city
    :param verbose: Verbose mode
    :return: The 2 cities of the tour that fit the constraint and the distance
    """
    logging.info(
        f"Nearest City To The Tour: Starting looking from the source list of cities nearest to {current_city.name}")
    if verbose:
        print("\n")
        print(
            f"\t \t Nearest City To The Tour: Starting looking from the source list of cities nearest to {current_city.name}")

    best_distance, best_city_prev, best_city_next = None, None, None
    # If we have one city into the tour the behaviour change
    if len(my_tour) == 1:
        logging.info("Nearest City To The Tour: There is only one city in the tour, only one calculation.")
        if verbose:
            print("\t \t Nearest City To The Tour: There is only one city in the tour, only one calculation.")
        best_distance = current_city.distance(my_tour[0])
        best_city_prev = my_tour[0]
        best_city_next = my_tour[0]
        logging.info(f"Nearest City To The Tour: Length {best_distance}")
        if verbose:
            print(f"\t \t \t Nearest City To The Tour: Length {best_distance}")
    else:
        # use a deep copy of the tour cities and add again the initial city for completing the cycle,
        # done for considering also the last arc!
        # the main insertion takes care only on prev_city so we don't have any such problem on doing this, so even if
        # in this local deep copy (remember copy() is deep only on the first layer of a collection) we have again the
        # initial city at the end, it will be (in case the criterion pick the last arc) the next_city (USELESS!)
        _city_list = my_tour.copy()
        _city_list.append(_city_list[0])
        for prev_city, next_city in zip(_city_list, _city_list[1:]):
            logging.info(f"Farthest City To The Tour: Try this shortcut {prev_city}-{current_city}-{next_city}")
            if verbose:
                print(f"\t \t \t Nearest City To The Tour: Try this shortcut {prev_city}-{current_city}-{next_city}")
            _distance_prev = current_city.distance(prev_city)
            _distance_next = current_city.distance(next_city)
            if verbose:
                print(f"\t \t \t Nearest City To The Tour: Length {_distance_prev + _distance_next}")
            if not best_distance:
                best_distance = _distance_prev + _distance_next
                best_city_prev = prev_city
                best_city_next = next_city

            if _distance_prev + _distance_next < best_distance:
                best_distance = _distance_prev + _distance_next
                best_city_prev = prev_city
                best_city_next = next_city

    logging.info(f"Nearest City To The Tour: The nearest addition is {best_city_prev}-{current_city}-{best_city_next}")
    if verbose:
        print(
            f"\t \t Nearest City To The Tour: The nearest addition is {best_city_prev}-{current_city}-{best_city_next}")
    return best_city_prev, best_city_next, best_distance


def maximum_min_distance_city_finder(instance: List[City], tour: Tour, verbose: bool = False) -> (City, City, City):
    """
    Evaluate the maximum among the nearest city of the instance over a tour
    :param instance: The city that are out of the tour
    :param tour: The current tour
    :param verbose: Verbose mode
    :return: Return the new city that it will be added to the tour, in this form (Previous city of the tour,City to add,
                Next city of the tour)
    """
    _nearest_list_ = []
    for city in instance:
        if verbose:
            print("\n")
            print(f"\t Maximum Minimum Distance: Find the nearest cut for {city}")
        tour_before_city, tour_after_city, distance = nearest_city_wrt_tour(tour.tour_cities, city, verbose=verbose)
        _nearest_list_.append((tour_before_city, city, tour_after_city, distance))
    # With this we retrieve the maximum of minimum distance
    _nearest_list_.sort(key=lambda element: element[3], reverse=True)
    return _nearest_list_[0][0], _nearest_list_[0][1], _nearest_list_[0][2]


def farthest_addition_algorithm(original_instance: List[City], initial_city: City = None, verbose: bool = False,
                                scatter: matplotlib.axes.Axes = None, graph_velocity: float = 0.01,
                                graph_step_by_step: bool = False) -> Tour:
    """
        Create a tour using the farthest addition criterion
        :param original_instance: The original instance of cities
        :param initial_city: (Optional) The initial city to start the tour
        :param verbose: Verbose mode
        :param scatter: If you want to plot the tour creation progress in another figure(defined outside)
        :param graph_velocity: The velocity on which the matplotlib figure is update in second
        :param graph_step_by_step: If True the figure showing is blocking, otherwise is no locking
        :return: A valid tour
    """
    logging.info(f"Farthest Addition: HELLO :=)")
    if verbose:
        print("\n")
        print(f"Farthest Addition: HELLO :=)")
    _tour: Tour = Tour(tour_type=original_instance[0].location_type, tour_name="Farthest Addition")

    # we select an initial city and remove it from the instance
    if verbose:
        print("Farthest Addition: Cloning list..")
    _instance: List[City] = original_instance.copy()

    if verbose:
        print("Farthest Addition: Setting up the initial instances")
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

    logging.info(f"Farthest Addition: Checking the starting point")
    logging.info(f"Farthest Addition: Original instance {original_instance}")
    logging.info(f"Farthest Addition: Starting city {_current_city.name}")
    logging.info(f"Farthest Addition: Starting Farthest Addition algorithm")
    if verbose:
        print(f"Farthest Addition: Start looking from the source list of cities nearest to {_current_city.name}")
        print(f"Farthest Addition: Checking the starting point..")
        print(f"Farthest Addition: Original instance {original_instance}")
        print(f"Farthest Addition: Starting city {_current_city.name}")
        print(f"Farthest Addition: Starting Farthest Addition algorithm..")

    # main loop to empty the set

    iterator_idx = 1
    while _instance:
        logging.info(f"Farthest Addition: Iteration {iterator_idx}, {_tour}")
        if verbose:
            print("\n")
            print(f"Farthest Addition: Iteration {iterator_idx}, {_tour}")
        prev_city, _current_city, after_city = maximum_min_distance_city_finder(_instance, _tour, verbose=verbose)

        logging.info(f"Farthest Addition: Adding {_current_city} to the tour")
        if verbose:
            print("\n")
            print(f"Farthest Addition: Adding {_current_city} to the tour")

        # move best city from the instance to the tour
        if prev_city == after_city:
            _tour.append(_current_city)
        else:
            _tour.add_after_city(_current_city, prev_city, verbose=verbose)
        _instance.remove(_current_city)
        iterator_idx += 1
        if verbose:
            plot_2d_tour(scatter=scatter, tour=_tour.tour_cities, instances=_instance, velocity=graph_velocity,
                         graph_step_by_step=graph_step_by_step)

    logging.info("Farthest Addition: Done.")
    logging.info(f"Farthest Addition: Checking if the tour is valid..")
    if verbose:
        print(f"Farthest Addition: Done.")
        print(f"Farthest Addition: Checking if the tour is valid..")

    # check if it is valid
    if not _tour.is_valid(original_instance):
        logging.error(f"Farthest Addition: Not valid.")
        if verbose:
            print(f"Farthest Addition: Not Valid.")
        return None

    logging.info("Farthest Addition: Ok.")
    logging.info(f"Farthest Addition: Tour length: {_tour.length():.3f}km")

    if verbose:
        plot_2d_tour(scatter=scatter, tour=_tour.tour_cities + [_tour.position(0)], instances=_instance,
                     velocity=graph_velocity,
                     graph_step_by_step=graph_step_by_step)
        print(f"Farthest Addition: Ok.")
        print(f"Farthest Addition: {_tour}")
        print(f"Farthest Addition: Tour length: {_tour.length():.3f}km")
    return _tour
