import logging
from Model.City import City
from Model.Tour import Tour
from Algorithm.NearestNeighbour import nearest_neighbor_algorithm
from Algorithm.FarthestAddition import farthest_algorithm_naive
verbose_mode = True
if __name__ == "__main__":
    logging.basicConfig(filename="DiMaioProject.log", level=logging.INFO,filemode="w")
    logging.info("Start")
    caserta : City = City(41.0842, 14.3358, "Caserta", verbose=verbose_mode)
    san_prisco: City = City(41.0881, 14.2791, "San Prisco", verbose=verbose_mode)
    ucraina: City = City(48.0881, 14.2791, "Ucraina", verbose=verbose_mode)
    perm: City = City(58.0000, 56.3166, "Perm", verbose=verbose_mode)

    logging.info("Finished")
    tour = nearest_neighbor_algorithm([caserta, ucraina, san_prisco, perm], None, verbose=verbose_mode)
    tour_2 = farthest_algorithm_naive([caserta,ucraina,san_prisco,perm],None,verbose=verbose_mode)
    tour.plot()
    tour_2.tour_name="Farthest Naive"
    tour_2.plot()