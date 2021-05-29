from Algorithm.LocalSearching.Evaluation.TwoOpt import delta_evaluation
from Model.Tour import Tour


def first_improvement_evaluation(tour: Tour, verbose=False) -> (int, int):
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
