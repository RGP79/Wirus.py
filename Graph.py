from matplotlib import pyplot as plt


class InputData:
    # wczytanie danych (dostaje filepath)
    pass


class Graph:
    def __init__(self, data):
        self.__data = data
        self.__graph = self.create_graph()

    def display_data(self):
        self.__graph.show()

    def create_graph(self):
        for country, data in self.__data:
            plt.semilogy(data, label=country)

        plt.xlabel("Kolejne dni")
        plt.ylabel("Liczba zainfekowanych")
        plt.title("Liczba chorych na Covid-19")
        plt.grid()
        plt.legend()
        plt.autoscale()

        return plt

    def save_graph(self):
        self.__graph.savefig("covid.pdf")
