from enum import Enum
from Model.City import City, CityDataType
from typing import List
import gspread


class InstanceSourceType(Enum):
    File = 0
    GoogleSheet = 1


class Instance:
    def __init__(self, instance_type: InstanceSourceType):
        self.loader_type = instance_type

    def __file_loader(self, path, verbose=False) -> List[City]:
        _instance = []
        if self.loader_type == InstanceSourceType.File:
            with open("./data sets/tsplib/dj38.tsp", "r") as file:
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
        return _instance

    def __online_loader(self, verbose=False):
        gc = gspread.service_account(filename="./no_dimaio_key.json")

        sh = gc.open("Network Optimization - Di Maio")
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

    def __file_writer(self, file_name, tour, verbose=False):
        with open(f"./{file_name}.csv", "w+") as file:
            file.write("city_name;coord_x;coord_y\n")
            for city in tour.tour_cities:
                file.write(f"{city.name};{city.get_coordinate()[0]};{city.get_coordinate()[1]}\n")

    def __online_writer(self, tour, verbose=False):
        gc = gspread.service_account(filename="./no_dimaio_key.json")

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

    def loader(self, path=None, verbose=False):
        if self.loader_type == InstanceSourceType.File:
            return self.__file_loader(path=path)
        else:
            return self.__online_loader()

    def writer(self, file_name, tour, verbose=False):
        if self.loader_type == InstanceSourceType.File:
            return self.__file_writer(file_name, tour, verbose=False)
        else:
            return self.__online_writer(tour, verbose=False)
