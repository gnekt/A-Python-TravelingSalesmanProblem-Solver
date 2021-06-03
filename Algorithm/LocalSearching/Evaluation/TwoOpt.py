#############################################
# Created by professor Marco Pranzo @ NO lAB 2021

from Model.Tour import Tour


def delta_evaluation(tour: Tour, pos1: int, pos3: int, verbose=False) -> bool:
    """
    Perform the delta evaluation for the 2-opt exchange
    :param tour: The current tour
    :param pos1: The position I target city
    :param pos3: The position J target city
    :param verbose: Verbose mode
    :return: (True) if the movement is a good one, (False) otherwise
    """
    c1 = tour.position(pos1)
    c2 = tour.position(pos1 + 1)
    c3 = tour.position(pos3)
    c4 = tour.position(pos3 + 1)
    if verbose:
        print(f"\t{c1}, {c2}")
        print(f"\t{c3}, {c4}")

    removed_costs = c1.distance(c2) + c3.distance(c4)
    added_costs = c1.distance(c3) + c2.distance(c4)
    if verbose:
        print(f"\tRemoving: {removed_costs}")
        print(f"\tAdding: {added_costs}")

    return removed_costs > added_costs