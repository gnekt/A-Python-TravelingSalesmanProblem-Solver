
from QuickPotato.profiling.intrusive import performance_test as pt
from QuickPotato.statistical.visualizations import FlameGraph

from FarthestAddition import farthest_addition_algorithm
from FarthestAdditionNaive import farthest_addition_algorithm_naive
from NearestAddition import  nearest_addition_algorithm
from NearestNeighbour import nearest_neighbor_algorithm
from Instance import Instance, InstanceSourceType

def testbench(instance):
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
        iteration=10,  # <-- The number of times you want to execute this method.
        pacing=0  # <-- How much seconds you want to wait between iterations.
    )

    FlameGraph(pt.test_case_name, test_id=pt.current_test_id).export("./")