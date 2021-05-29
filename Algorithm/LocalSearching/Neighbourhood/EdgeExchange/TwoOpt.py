from Model.Tour import Tour


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
