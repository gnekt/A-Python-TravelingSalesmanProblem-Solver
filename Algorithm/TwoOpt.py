#############################################
# Coded by the professor Marco Pranzo @ 2021 NO Lab
#
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


def move2opt(tour: Tour, pos1: int, pos3: int, verbose=False) -> Tour:
    """
    Perform the 2-opt exchange
    :param tour: The current tour
    :param pos1: The position I target city
    :param pos3: The position J target city
    :param verbose: Verbose mode
    :return: The re-arranged tour
    """
    # build the three segments
    segment1 = tour.tour_cities[:(pos1 + 1)]
    segment2 = tour.tour_cities[(pos1 + 1):(pos3 + 1)]
    segment3 = tour.tour_cities[(pos3 + 1):]
    # reverse the segment2
    segment2.reverse()
    if verbose:
        print(f"T: {tour.tour_cities}")
        print(f"S1: {segment1}")
        print(f"S2: {segment2}")
        print(f"S3: {segment3}")
    # to join the segments
    tour.tour_cities = segment1 + segment2 + segment3
    if verbose:
        print(tour)
    return tour


def first_improvement_evaluation(tour: Tour, verbose=False) -> (int,int):
    """
    Perform the first improvement exploration of neighbour
    :param tour: The current tour
    :param verbose: Verbose mode
    :return: The neighbour which improve, in term of position in the tour (int,int)->(i,j)city
    """
    """Look for the first improvement. Return pos1 and pos3"""
    for pos1 in range(int(len(tour.tour_cities) - 3)):
        for pos3 in range(pos1 + 2, len(tour.tour_cities) - 1):
            if pos1 != 0 or pos3 + 1 != len(tour.tour_cities) - 1:
                if verbose:
                    print(f"Checking {pos1} {pos3}")
                if delta_evaluation(tour, pos1, pos3, verbose):
                    if verbose:
                        print(f"Found an improvement {pos1} {pos3}")
                    return pos1, pos3
                elif verbose:
                    print(f"Not improving {pos1} {pos3}")
    if verbose:
        print("Found Local Minimum")
    return None, None
