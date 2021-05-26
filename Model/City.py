import random

from Model import geolocator
from geopy.distance import geodesic
import logging


class City:
    """
        Class which define a city, it will contain:
        - A city name
        - The coordinate in terms of latitude and longitude (DD format)
    """

    def __init__(self, lat: float, long: float, city_name: str, verbose: bool = False):
        """
        Constructor of the class
        :param lat: The latitude in DD format
        :param long: The longitude in DD format
        :param city_name: The name of the City
        :param verbose: Verbose modality
        :exception: If the latitude or longitude are not in the format of DD or the exceed their value
        :exception: If the name of the city is empty or not passed
        """
        logging.info("City: Starting to initialize a city..")
        if not city_name or city_name == "":
            raise ValueError("City name not initialized")
        logging.info(f"City: City name: {city_name}")

        if verbose:
            print("Starting to initialize a city..")
            print(f"City name: {city_name}")

        if not type(lat) is float or not type(long) is float:
            raise TypeError(f"Wrong coordinates type, got lat:{lat}, long:{long}")

        if not (-90 <= lat <= 90) or not (-180 <= long <= 180):
            raise ValueError(f"Wrong coordinates value, got lat:{lat}, long:{long}")

        logging.info(f"City: Coordinates: {lat},{long}")
        if verbose:
            print(f"Coordinates: {lat},{long}")

        try:
            self.location = geolocator.reverse(f"{lat}, {long}")
            self.name = city_name
        except Exception as ex:
            print(ex)
            logging.exception(ex, exc_info=True)
        logging.info("City: Created.")

        if verbose:
            print("Created")

    def __repr__(self):
        return f"{self.name}"

    def __eq__(self, other_city):
        return self.location == other_city.location



    def distance(self, other_city, unit_of_measure: str = "km", verbose: bool = False) -> float:
        """
        Retrieve the distance using the geodesic distance *ref geopy*
        :param verbose: Verbose modality
        :param unit_of_measure: The unit of measurement that we want to retrieve, km as default
        :param other_city: The other city as object of City, which we want to retrieve the distance
        :return: The distance between this two city
        :type other_city: City
        :exception: If other_city is not class City return an exception
        """
        logging.info(f"City: Requested a distance measuring from {self.name}..")
        logging.info(f"City: Checking if the other city to consider is a city..")

        if verbose:
            print(f"City: Requested a distance measuring from {self.name}..")
            print(f"City: Checking if the other city to consider is a city..")

        if type(other_city) is not City:
            return TypeError("Wrong type of other city")

        logging.info("City: Ok")
        logging.info(f"City: Computing the geodesic distance between {self.name} and {other_city.name}")

        if verbose:
            print("Ok")
            print(f"Computing the geodesic distance between {self.name} and {other_city.name}")

        try:
            _distance = geodesic((self.location.latitude,self.location.longitude),(other_city.location.latitude,other_city.location.longitude))
        except Exception as ex:
            logging.exception("City: An error occurred during the computation of the distance", ex, exc_info=True)

        _distance = _distance.kilometers if unit_of_measure == "km" else _distance.miles

        logging.info(f"City: Distance computed, equal: {_distance:.3f}{unit_of_measure}")

        if verbose:
            print("Distance computed, equal: {_distance:.3f}{unit_of_measure}")

        return _distance