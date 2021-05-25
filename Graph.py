from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Figure

COUNTRY_COLUMN_ID = 1


# wczytanie danych
class ReadCountries:
    def __init__(self, filepath):
        self.__countries = []
        self.__read_countries(filepath)

    def __read_countries(self, filepath):

        with open(filepath, "r") as f:
            for line in f:
                if line[0] == ",":
                    maybe_country = line.split(",")[COUNTRY_COLUMN_ID]
                    self.__countries.append(maybe_country)

    def get_countries(self):
        return self.__countries


class PatientsVector:
    def __init__(self, line):
        self.__vector = []
        self.__get_patients_as_vector(line)

    def __get_patients_as_vector(self, country_data_line):
        n_of_unimportant_column = 4
        if country_data_line[0:2] == ',"':
            n_of_unimportant_column = 5
        n_of_patients_in_time = country_data_line.split(",")[n_of_unimportant_column:]
        n_of_patients_in_time = [int(val) for val in n_of_patients_in_time]

        self.__vector = n_of_patients_in_time

    def get_vector(self):
        return self.__vector


class ReadData:
    def __init__(self, filepath, countries, start_day):
        self.__data = []
        self.__read_countries_data(filepath, countries, start_day)

    def __read_countries_data(self, filepath, countries, start_day):
        countries_data = dict()

        with open(filepath, "r") as f:
            for line in f:
                if line[0] == ",":
                    maybe_country = line.split(",")[COUNTRY_COLUMN_ID]
                    if maybe_country in countries:
                        line = line.strip()
                        n_of_patients_in_time = PatientsVector(line).get_vector()

                        countries_data[maybe_country] = n_of_patients_in_time[start_day:]

        self.__data = countries_data

    def get_data(self):
        return self.__data


class ReadLen:
    def __init__(self, filepath):
        self.__len = None
        self.__read_len(filepath)

    def __read_len(self, filepath):
        with open(filepath, "r") as f:
            for line in f:
                if line[0] == ",":
                    line = line.strip()
                    country_list = PatientsVector(line).get_vector()
                    break
        self.__len = len(country_list)

    def get_len(self):
        return self.__len


class Graph(Figure):
    def __init__(self, data, start_day):
        fig, self.ax = plt.subplots(figsize=(7, 5), dpi=200)
        super().__init__(fig)
        self.create_graph(data, start_day)

    def create_graph(self, n_of_patients_in_countries, start_day):
        x = []
        for i in range(414 - start_day):
            x.append(int(start_day + i + 1))

        for country, data in n_of_patients_in_countries.items():
            self.ax.semilogy(x, data, label=country)
        self.ax.legend()
        self.ax.set_xlim([start_day, 414])
        self.ax.set_title("Wykres zachorowań")
        self.ax.set_xlabel("Liczba dni")
        self.ax.set_ylabel("liczba zachorowań")
