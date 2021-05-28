#############################################
# Created by Christian Di Maio, github : @christiandimaio
# v 0.1
from enum import Enum
from math import sqrt
from Model import geolocator
from geopy.distance import geodesic
import logging


class CityDataType(Enum):
    Geographical = 1
    Euclidian_2D = 2


class City:
    """
        Class which define a city, it will contain:
        - A city name
        - The coordinate in terms of latitude and longitude (DD format)
    """

    def __init__(self,
                 location_info_type: CityDataType,
                 coord_x: float,
                 coord_y: float,
                 city_name: str,
                 verbose: bool = False):
        """
        Constructor of the class
        :param location_info_type: Tell which representation is used for the coordinates Geographical or Euclidian_2D
        :param coord_x: The longitude in Geographical format, or the X-axis in Euclidian_2D format
        :param coord_y: The latitude in Geographical format, or the Y-axis in Euclidian_2D format
        :param city_name: The name of the City
        :param verbose: Verbose modality
        :exception: If the latitude or longitude are not in the format of Geo or they exceed their value
        :exception: If the name of the city is empty or not passed
        """
        logging.info("City: Starting to initialize a city..")
        if not city_name or city_name == "":
            raise ValueError("City name not initialized")
        logging.info(f"City: City name: {city_name}")

        if verbose:
            print("Starting to initialize a city..")
            print(f"City name: {city_name}")
            print(f"City is represented by {location_info_type.name} Type")
            print("Checking coordinates..")

        self.location_type = location_info_type

        # Check if the coordinates are valid
        if self.location_type == CityDataType.Geographical:
            if not type(coord_y) is float or not type(coord_x) is float:
                raise TypeError(f"Wrong coordinates type, got lat:{coord_y}, long:{coord_x}")

            if not (-90 <= coord_y <= 90) or not (-180 <= coord_x <= 180):
                raise ValueError(f"Wrong coordinates value, got lat:{coord_y}, long:{coord_x}")

            try:
                self.__location = geolocator.reverse(f"{coord_y}, {coord_x}")
            except Exception as ex:
                print(ex)
                logging.exception(ex, exc_info=True)
        else:
            if not type(coord_y) is float or not type(coord_x) is float:
                raise TypeError(f"Wrong coordinates type, got x:{coord_x}, y:{coord_y}")
            self.__location = (coord_x, coord_y)

        logging.info(f"City: Coordinates: {self.get_coordinate()}")
        if verbose:
            print(f"Coordinates: {self.get_coordinate()}")

        self.name = city_name
        logging.info("City: Created.")

        if verbose:
            print("Created")

    def get_coordinate(self):
        """
        Getter for the coordinate, since we have two type of representation, is needed.
        :return: Coordinate as (X,Y) if CityDataType is Eucledian, (Latitude,Longitude) if Geographical.
        """
        if self.location_type == CityDataType.Euclidian_2D:
            return self.__location[0], self.__location[1]
        if self.location_type == CityDataType.Geographical:
            return self.__location.latitude, self.__location.longitude

    def __repr__(self):
        """
        Representation of a city in term of its name.
        :return:
        """
        return f"{self.name}"

    def __eq__(self, other_city):
        """
        Equal over-ride, two cities are equal if the belongs to the same coordinates
        :param other_city: The other city to evaluate
        :return: a bool object which represent if the statement holds or not
        """
        if not other_city.location_type == self.location_type:
            return False
        if self.location_type == CityDataType.Euclidian_2D:
            return self.get_coordinate() == other_city.get_coordinate()
        if self.location_type == CityDataType.Geographical:
            return self.__location.latitude == other_city.__location.latitude and \
                        self.__location.longitude == other_city.__location.longitude
        return False

    def distance(self, other_city, unit_of_measure: str = "km", verbose: bool = False) -> float:
        """
        Retrieve the distance -> using the geodesic distance *ref geopy* if the coordinates are type Geographical
                              -> euclidean distance if the coordinates are Euclidian_2D
        :param verbose: Verbose modality
        :param unit_of_measure: The unit of measurement that we want to retrieve, km as default (Useless for coord_type EUC_2D)
        :param other_city: The other city which we want to retrieve the distance
        :return: The distance between this two city
        :type other_city: City
        :exception: If other_city is not class City return an exception
        """
        logging.info(f"City: Requested a distance {self.name}-{other_city.name}")
        logging.info(f"City: Checking if the other city to consider is a city..")

        if type(other_city) is not City:
            return TypeError("Wrong type of other city")

        if other_city.location_type != self.location_type:
            return TypeError("The distance can't be computed since they are using two differents point representation\n"
                             f"{self.name}: {self.location_type.name}, {other_city.name}: {other_city.location_type.name}")

        logging.info("Cities: Ok")
        _distance = 0.0
        if self.location_type == CityDataType.Geographical:
            logging.info(f"City: Computing the geodesic distance between {self.name} and {other_city.name}")

            try:
                _other_city_latitude, _other_city_longitude = other_city.get_coordinate()
                _distance = geodesic((self.__location.latitude, self.__location.longitude),
                                     (_other_city_latitude, _other_city_longitude))
                _distance = _distance.kilometers if unit_of_measure == "km" else _distance.miles
            except Exception as ex:
                logging.exception("City: An error occurred during the computation of the distance", ex, exc_info=True)
        else:
            logging.info(f"City: Computing the eucledian distance between {self.name} and {other_city.name}")

            try:
                _local_city_x, _local_city_y = self.get_coordinate()
                _other_city_x, _other_city_y = other_city.get_coordinate()
                _distance = sqrt((_local_city_x - _other_city_x) ** 2 + (_local_city_y - _other_city_y) ** 2)
            except Exception as ex:
                logging.exception("City: An error occurred during the computation of the distance", ex, exc_info=True)

        logging.info(
            f"City: Distance computed, equal: {_distance:.3f}{unit_of_measure if self.location_type == CityDataType.Geographical else ''}")

        return _distance
