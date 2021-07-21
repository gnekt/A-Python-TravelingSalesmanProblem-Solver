#############################################
# Created by Christian Di Maio, github : @christiandimaio
# v 0.1
import json
import os
from enum import Enum
from Model.City import City, CityDataType
from typing import List
import gspread
import logging
from Tour import Tour


class InstanceSourceType(Enum):
    """
    Enumerator for defining the type of the source file
    """
    File = 0  # It comes from a file
    GoogleSheet = 1  # It comes from google sheet


class Instance:
    """
    Class which represent the instance creator, it will allow to read and write a collection of city
        Into two different way, according to InstanceSourceType
    """

    def __init__(self, instance_type: InstanceSourceType):
        """
        Constructor for the class
        :param instance_type: Tell if we are dealing with file or with google sheet source
        """
        self.loader_type = instance_type

    # To-Do1 -> Add a way for loading also other type of file structure, json(?)
    def __file_loader(self, path: str, verbose: bool = False) -> List[City]:
        """
        Private method for loading an instance from file.

        :param path: The path of the file (could be also relative)
        :param verbose: Verbose Mode
        :return: The instance as a list of City
        """
        _instance = []
        if self.loader_type == InstanceSourceType.File:
            try:
                filename, file_extension = os.path.splitext(path)
            except FileNotFoundError as ex:
                logging.exception("File not found", exc_info=True)
            with open(path, "r") as file:
                if file_extension == ".tsp":
                    _coordinate_types = CityDataType.Euclidian_2D
                    while file:
                        line = file.readline()
                        if line == "":
                            break
                        if "EDGE_WEIGHT_TYPE" in line:
                            detect = line.split(sep=":")[1].strip()
                            if detect != "EUC_2D":
                                raise TypeError("Sadly for TSPLIB the only supported type is Euclidean 2D :("
                                                ", if you want use latitude and longitude you need to find another "
                                                "representation, see the docs")

                            continue
                        if "NODE_COORD_SECTION" not in line:
                            continue
                        # Inizio lettura
                        for city in file.readlines():
                            name, x, y = [number.replace("\n", "") for number in city.split(" ")]
                            _instance.append(City(location_info_type=_coordinate_types,
                                                  coord_x=float(x),
                                                  coord_y=float(y),
                                                  city_name=str(name), verbose=verbose))
                if file_extension == ".json":
                    instance_raw = json.load(file)
                    for city in instance_raw:
                        _instance.append(City(location_info_type=CityDataType.Geographical,
                                              city_name=str(city),
                                              coord_y=float(instance_raw[city]['lat']),
                                              coord_x=float(instance_raw[city]['long']),
                                              verbose=verbose))

        return _instance

    def __online_loader(self, sheet: str = "Network Optimization - Di Maio", verbose: bool = False) -> List[City]:
        """
        Private method for loading an instance from google sheet
        :param sheet: The source sheet, for the purpose of the project the only admitted sheet is the default one.
        :param verbose: Verbose Mode
        :return:
        """
        # The key file is generated using a google developer account, replace with your own one, if you want this kind
        #   of features.
        gc = gspread.service_account(filename="./api_key.json")
        sh = gc.open(sheet)
        worksheet = sh.worksheet("Loader")
        coordinates_type = CityDataType.Euclidian_2D \
            if worksheet.col_values(4)[0] == CityDataType.Euclidian_2D.name \
            else CityDataType.Geographical

        name = worksheet.col_values(1)
        coordinates_x = worksheet.col_values(2)
        coordinates_y = worksheet.col_values(3)
        _instance = []
        for name, coord_x, coord_y in zip(name, coordinates_x, coordinates_y):
            _instance.append(City(location_info_type=coordinates_type,
                                  coord_x=float(coord_x),
                                  coord_y=float(coord_y),
                                  city_name=str(name), verbose=verbose))
        return _instance

    def __file_writer(self, file_name: str, tour: Tour, verbose: bool = False):
        """
        Private method for writing a tour on a file.
            v0.1 = It allows only TSPLIB file format

        :param file_name: The name of the output file
        :param tour: The tour to be written
        :param verbose: Verbose Mode
        """
        with open(f"./{file_name}.csv", "w+") as file:
            file.write("city_name coord_x coord_y\n")
            for city in tour.tour_cities:
                file.write(f"{city.name} {city.get_coordinate()[0]} {city.get_coordinate()[1]}\n")

    def __online_writer(self, tour: Tour, verbose: bool = False):
        """
        Private method for writing a tour on a google sheet.
            v0.1 = It allows only TSPLIB file format

        :param tour: The tour to be written
        :param verbose: Verbose Mode
        """
        gc = gspread.service_account(filename="./api_key.json")

        sh = gc.open("Network Optimization - Di Maio")
        worksheet = sh.worksheet("Writer")
        _tour = [[city.name,
                  city.get_coordinate()[0],
                  city.get_coordinate()[1]] for city in tour.tour_cities]
        cells = []
        for row_num, row in enumerate(_tour):
            for col_num, cell in enumerate(row):
                cells.append(gspread.Cell(row_num + 1, col_num + 1, _tour[row_num][col_num]))

        worksheet.update_cells(cells)

    def loader(self, path: str = None, gsheet_name: str = "Network Optimization - Di Maio", verbose: bool = False) -> \
    List[City]:
        """
        Public mask for loading an instance from a source (either File or GSheet)
        :param path: [LOADER TYPE: FILE] The path of the file (could be also relative)
        :param gsheet_name: [LOADER TYPE: GSHEET] The name of the google sheet.
        :param verbose: Verbose Mode
        """
        if self.loader_type == InstanceSourceType.File:
            return self.__file_loader(path=path)
        else:
            return self.__online_loader(sheet=gsheet_name)

    def writer(self, file_name: str, tour: Tour, verbose: bool = False):
        """
        Public mask for loading an instance from a source (either File or GSheet)
        :param file_name: [LOADER TYPE: FILE] The path of the file (could be also relative)
        :param tour: The tour to be written
        :param verbose: Verbose Mode
        """
        if self.loader_type == InstanceSourceType.File:
            return self.__file_writer(file_name, tour, verbose=False)
        else:
            return self.__online_writer(tour, verbose=False)
