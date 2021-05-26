import logging
from Model.City import City
from Model.Tour import Tour
from Model.City import CityDataType as CoordinateType
from Algorithm.NearestNeighbour import nearest_neighbor_algorithm
from Algorithm.FarthestAdditionNaive import farthest_algorithm_naive
from Algorithm.FarthestAddition import farthest_algorithm
from Algorithm.NearestAddition import nearest_addition_algorithm
verbose_mode = True
if __name__ == "__main__":
    logging.basicConfig(filename="DiMaioProject.log", level=logging.INFO,filemode="w")
    logging.info("Start")
    caserta : City = City(CoordinateType.Geographical, 14.3358, 41.0842, "Caserta", verbose=verbose_mode)
    san_prisco: City = City(CoordinateType.Geographical, 20.2791, 41.0881, "San Prisco", verbose=verbose_mode)
    ucraina: City = City(CoordinateType.Geographical, 14.2791, 48.0881, "Ucraina", verbose=verbose_mode)
    perm: City = City(CoordinateType.Geographical, 56.3166, 58.0000, "Perm", verbose=verbose_mode)

    logging.info("Finished")
    tour = nearest_neighbor_algorithm([caserta, ucraina, san_prisco, perm], None, verbose=verbose_mode)
    tour_2 = farthest_algorithm_naive([caserta,ucraina,san_prisco,perm],None,verbose=verbose_mode,graph_velocity=1,graph_step_by_step=False)
    tour_3 = farthest_algorithm([caserta,ucraina,san_prisco,perm],None,verbose=verbose_mode,graph_velocity=1,graph_step_by_step=False)
    tour_4 = nearest_addition_algorithm([caserta,ucraina,san_prisco,perm],None,verbose=verbose_mode,graph_velocity=1,graph_step_by_step=False)
    tour.plot()
    tour_2.tour_name="Farthest Naive"
    tour_2.plot()
    tour_3.tour_name = "Farthest"
    tour_3.plot()
    tour_4.tour_name = "Nearest Addition"
    tour_4.plot()