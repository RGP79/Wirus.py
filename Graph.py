from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Figure

COUNTRY_COLUMN_ID = 1


# wczytanie danych (dostaje filepath)
def read_countries(filepath):
    countries = []

    with open(filepath, "r") as f:
        for line in f:
            if line[0] == ",":
                maybe_country = line.split(",")[COUNTRY_COLUMN_ID]
                countries.append(maybe_country)
    return countries


def get_patients_as_vector(country_data_line):
    n_of_unimportant_column = 4
    if country_data_line[0:2] == ',"':
        n_of_unimportant_column = 5
    n_of_patients_in_time = country_data_line.split(",")[n_of_unimportant_column:]
    n_of_patients_in_time = [int(val) for val in n_of_patients_in_time]

    return n_of_patients_in_time


def read_countries_data(filepath, countries):
    countries_data = dict()

    with open(filepath, "r") as f:
        for line in f:
            if line[0] == ",":
                maybe_country = line.split(",")[COUNTRY_COLUMN_ID]
                if maybe_country in countries:
                    line = line.strip()
                    n_of_patients_in_time = get_patients_as_vector(line)
                    countries_data[maybe_country] = n_of_patients_in_time
    return countries_data


class Graph(Figure):
    def __init__(self, data):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(fig)
        self.create_graph(data)


    def display_graph(self):
        self.__graph.show()

    def create_graph(self, n_of_patients_in_countries):
        for country, data in n_of_patients_in_countries.items():
            self.ax.semilogy(data, label=country)
        self.ax.legend()




    def save_graph(self):
        self.__graph.savefig("covid.pdf")
