from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Figure


class InputData:
    # wczytanie danych (dostaje filepath)
    pass


class Graph(Figure):
    def __init__(self):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(fig)

    def display_graph(self):
        self.__graph.show()

    def create_graph(self, n_of_patients_in_countries):
        for country, data in n_of_patients_in_countries.items():
            self.ax.semilogy(data, label=country)

        self.ax.xlabel("Kolejne dni")
        self.ax.ylabel("Liczba zainfekowanych")
        self.ax.title("Liczba chorych na Covid-19 (od 01.01.2020)")
        self.ax.grid()
        self.ax.legend()
        self.ax.autoscale()


    def save_graph(self):
        self.__graph.savefig("covid.pdf")


