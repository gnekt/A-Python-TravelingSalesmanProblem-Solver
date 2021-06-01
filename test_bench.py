
from QuickPotato.profiling.intrusive import performance_test as pt
from QuickPotato.statistical.visualizations import FlameGraph

from ConstructiveHeuristic.FarthestAddition import farthest_addition_algorithm
from ConstructiveHeuristic.FarthestAdditionNaive import farthest_addition_algorithm_naive
from ConstructiveHeuristic.NearestAddition import  nearest_addition_algorithm
from ConstructiveHeuristic.NearestNeighbour import nearest_neighbor_algorithm

from Instance import Instance, InstanceSourceType
from LocalSearch import NeighborhoodType, ExplorationType, LocalSearch


def local_search(instance):
    local_search = LocalSearch(neighbourhood=NeighborhoodType.TWO_OPT, exploration=ExplorationType.FIRST_IMPROVEMENT)
    local_search.local_search(original_instance=instance,constructive_algorithm=farthest_addition_algorithm_naive)
    local_search.local_search(original_instance=instance, constructive_algorithm=farthest_addition_algorithm)
    local_search.local_search(original_instance=instance, constructive_algorithm=nearest_addition_algorithm)
    local_search.local_search(original_instance=instance, constructive_algorithm=nearest_neighbor_algorithm)

def testbench(instance):
    #local_search(instance)
    farthest_addition_algorithm_naive(original_instance=instance)
    farthest_addition_algorithm(original_instance=instance)
    nearest_addition_algorithm(original_instance=instance)
    nearest_neighbor_algorithm(original_instance=instance)

if __name__ == "__main__":
    # Create a test case
    interface = Instance(instance_type=InstanceSourceType.File)
    instance = interface.loader("./data sets/tsplib/dj38.tsp", verbose=False)
    pt.test_case_name = "exporting to csv"

    pt.measure_method_performance(
        method=testbench,  # <-- The Method which you want to test.
        arguments=[instance],  # <-- Your arguments go here.
        iteration=1,  # <-- The number of times you want to execute this method.
        pacing=0  # <-- How much seconds you want to wait between iterations.
    )

    FlameGraph(pt.test_case_name, test_id=pt.current_test_id).export("./")