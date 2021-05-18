from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Figure


class InputData:
    # wczytanie danych (dostaje filepath)
    pass


class Graph(Figure):
    def __init__(self, n_of_patients_in_countries):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        self.__n_of_patients_in_countries = n_of_patients_in_countries
        super().__init__(fig)
        self.__graph = self.create_graph()


    def create_graph(self):
        for country, data in self.__n_of_patients_in_countries.items():
            plt.semilogy(data, label=country)

        plt.xlabel("Kolejne dni")
        plt.ylabel("Liczba zainfekowanych")
        plt.title("Liczba chorych na Covid-19 (od 01.01.2020)")
        plt.grid()
        plt.legend()
        plt.autoscale()
        # plt.draw()
        return plt

    def __repr__(self):
        return self.__graph
        #
        # data = [random.random() for i in range(50)]
        # ax = self.figure.add_subplot(111)
        # ax.plot(data, 'r-')
        # ax.set_title('PyQt Matplotlib Example')



    def save_graph(self):
        self.__graph.savefig("covid.pdf")



