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


def read_countries_data(filepath, countries, start_day):
    countries_data = dict()

    with open(filepath, "r") as f:
        for line in f:
            if line[0] == ",":
                maybe_country = line.split(",")[COUNTRY_COLUMN_ID]
                if maybe_country in countries:
                    line = line.strip()
                    n_of_patients_in_time = get_patients_as_vector(line)
                    print(len(n_of_patients_in_time))
                    countries_data[maybe_country] = n_of_patients_in_time[start_day:]
    return countries_data


def read_len(filepath):
    with open(filepath, "r") as f:
        for line in f:
            if line[0] == ",":
                line = line.strip()
                country_list = get_patients_as_vector(line)
                break
    return len(country_list)


class Graph(Figure):
    def __init__(self, data, start_day):
        fig, self.ax = plt.subplots(figsize=(7, 5), dpi=200)
        super().__init__(fig)
        self.create_graph(data, start_day)


    def display_graph(self):
        self.__graph.show()

    def create_graph(self, n_of_patients_in_countries, start_day):
        x = []
        for i in range(414 - start_day):
            x.append(int(start_day + i + 1))

        for country, data in n_of_patients_in_countries.items():
            self.ax.semilogy(x, data, label=country)
        self.ax.legend()
        self.ax.set_xlim([start_day, 414])
        self.ax.set_title("Wykres zachorowań")


    def save_graph(self):
        self.__graph.savefig("covid.pdf")
