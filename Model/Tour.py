import webbrowser
from typing import  List
from Model.City import City
import logging
import folium
from Model.City import CityDataType
import warnings

class Tour:
    """
    Class which represent the tour (hamiltonian cycle) solving a TSP.
    """
    def __init__(self, tour_type: CityDataType, tour_name: str = "Tour", verbose: bool = False):
        """
        Constructor of the tour, it will start empty if no instance is loaded.
        :param tour_name: The name of the tour
        :param verbose: Verbose mode
        """
        logging.info(f"Tour: Tour {tour_name} created")
        logging.info(f"Tour: Tour with city position coordinates as {tour_type.name}")
        if verbose:
            print(f"Tour {tour_name} created")
        self.tour_type = tour_type
        self.tour_cities = []
        self.tour_name = tour_name

    def __repr__(self):
        return str(f"Tour: {self.tour_cities}")

    def append(self, new_city: City, verbose: bool = False) -> bool:
        """
        Add at the end of the tour a new city
        :param verbose: Verbose mode
        :param new_city: The city that we want to add
        :return: True if the appending is successful, otherwise False
        """
        logging.info("Tour: Adding a new city to the tour")
        logging.info("Tour: Checking if the new city is valid..")

        if type(new_city) is not City:
            raise TypeError("The city that you want to add is not a City object")

        if new_city.location_type != self.tour_type:
            raise TypeError("The city that you want to add has a different coordinates representation"
                            f"Tour: {self.tour_type.name}, City: {new_city.location_type.name}")

        if len(self.tour_cities) > 1 and new_city == self.tour_cities[0]:
            warnings.warn("Hey it looks like you want add again the initial city, maybe you want to represent the cycle\n"
                          "But pay attention, all the algorithm treat the tour as a path that doesn't include at the end\n"
                          "The starting point.\n"
                          "So from now on, i can't guarantee the correctness of the solution, be aware of doing something"
                          "Without thinking. Thank you :)")

        if new_city in self.tour_cities and new_city != self.tour_cities[0]:
            raise ValueError("The city that you want to add is already in the tour")

        self.tour_cities.append(new_city)

        logging.info("Tour: Ok.")
        return True

    def add_after_city(self, new_city: City, target_city: City, verbose: bool = False) -> bool:
        """
        Add a city after a target city already in the tour
        :param new_city: The new city which we want to add
        :param target_city: The city that will be used as target
        :param verbose: Verbose mode
        :return: True if the appending is successful, otherwise False
        """
        logging.info(f"Tour: Adding a new city to the tour, after a target one.")
        logging.info(f"Tour: Checking if the target city is valid..")

        if type(target_city) is not City:
            raise TypeError("The city target is not a City object")

        if target_city not in self.tour_cities:
            raise ValueError("The city target is not in the tour")

        logging.info("Tour: Checking if the new city is valid..")

        if type(new_city) is not City:
            raise TypeError("The city that you want to add is not a City object")

        if new_city.location_type != self.tour_type:
            raise TypeError("The city that you want to add has a different coordinates representation"
                            f"Tour: {self.tour_type.name}, City: {new_city.location_type.name}")

        if len(self.tour_cities) > 1 and new_city == self.tour_cities[0]:
            warnings.warn("Hey it looks like you want add again the initial city, maybe you want to represent the cycle\n"
                          "But pay attention, all the algorithm treat the tour as a path that doesn't include at the end\n"
                          "The starting point.\n"
                          "So from now on, i can't guarantee the correctness of the solution, be aware of doing something"
                          "Without thinking. Thank you :)")

        if new_city in self.tour_cities and new_city != self.tour_cities[0]:
            raise ValueError("The city that you want to add is already in the tour")

        self.tour_cities.insert(self.tour_cities.index(target_city)+1,new_city)
        logging.info("Tour: Ok.")
        return True

    def length(self, unit_of_measurement: str = "km") -> float:
        """
        Compute the length of the tour, in *unit_of_meausurement* if tour type is Geographical
        :return: The length of the tour
        """
        _length = 0.0
        prev_city = self.tour_cities[0]

        for c in self.tour_cities[1:]:
            _length += prev_city.distance(c)
            prev_city = c
        # Assuming that even it is passed to distance the unit of measure, if they are euclidian this
        #       parameter is skipped, so to abbreviate the code we can remain it without if and we are sure
        #           that it works. :)
        _length += prev_city.distance(self.tour_cities[0],unit_of_measure=unit_of_measurement)
        return _length

    def is_valid(self, instance: List[City]) -> bool:
        """
        Check if a tour is valid
        :param instance: The instance with all the city on which we want create a tour
        :return: True if the statement holds, otherwise False
        """
        if (len(self.tour_cities) == len(instance)) and all(city in instance for city in self.tour_cities):
            return True
        return False

    def plot(self):
        _complete_tour = self.tour_cities.copy()
        _complete_tour.append(self.tour_cities[0])
        m = folium.Map(location=_complete_tour[0].get_coordinate())
        folium.Marker(_complete_tour[0].get_coordinate(),
                      icon=folium.Icon(color="red", prefix='fa', icon="car")).add_to(m)
        for city in _complete_tour[1:-1]:
            folium.Marker(city.get_coordinate(),
                      icon=folium.Icon(color="green",prefix='fa',icon="info-circle")).add_to(m)
        folium.PolyLine([(city.get_coordinate()) for city in _complete_tour],color="red"
                            ,weight=2).add_to(m)
        m.save(f"{self.tour_name}.html")
        webbrowser.open(f"{self.tour_name}.html", new=2)

    def position(self, position_number):
        """Return the city in the requested position"""
        if position_number < 0 or position_number >= len(self.tour_cities):
            raise Exception(f"ERROR: Accessing outside the tour ({position_number})")
        return self.tour_cities[position_number]

    def remove(self, position_number):
        """Remove a city from the tour based on the position"""
        del self.tour_cities[position_number]