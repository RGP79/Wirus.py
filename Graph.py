from io import BytesIO
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Figure
from Exceptions import ErrorWindow
from File_service import ReadData

class Graph(Figure):
    __IMG_FORMAT = "png"

    def __init__(self, data, start_day, end_day, parent):
        self.fig, self.ax = plt.subplots(figsize=(7, 5), dpi=160)
        super().__init__(self.fig)
        self.type = parent.get_type()
        self.__parent = parent
        self.create_graph(data, start_day, end_day)

    def create_graph(self, n_of_patients_in_countries, start_day, end_day):
        print(n_of_patients_in_countries)
        x = []
        for i in range(end_day - start_day):
            x.append(start_day + i)

        for country, data in n_of_patients_in_countries.items():
            self.ax.semilogy(x, data, label=country)

        self.ax.legend()

        self.ax.set_xlim([start_day, end_day])
        if self.type == "chorzy":
            self.ax.set_title("Wykres zachorowań")
            self.ax.set_ylabel("Liczba zachorowań")
        elif self.type == "zdrowi":
            self.ax.set_title("Wykres ozdrowień")
            self.ax.set_ylabel("Liczba ozdrowień")
        self.ax.set_xlabel("Liczba dni")

    def get_img(self):
        img_data = BytesIO()
        self.fig.savefig(img_data, format=self.__IMG_FORMAT)
        seek_offset = 0
        img_data.seek(seek_offset)

        return img_data


class UpdateGraph:
    def __init__(self, parent):
        self.__type = parent.get_type()
        self.__parent = parent
        self.__cos()

    def __cos(self):
        try:
            print(f"to jest end day {self.__parent.Data.END_DAY}")
            data = ReadData(self.__parent.Data.FILENAME, self.__parent.Data.COUNTRIES_CLICKED,
                            self.__parent.Data.START_DAY, self.__parent.Data.END_DAY).get_data()
            plot = Graph(data, self.__parent.Data.START_DAY, self.__parent.Data.END_DAY, self.__parent)
            self.__parent.main_layout.removeWidget(self.__parent.get_graph())
            self.__parent.main_layout.addWidget(plot, 0, 0, 4, 3)
            self.__parent.setLayout(self.__parent.main_layout)

        except:
            ErrorWindow("Nie wybrano pliku lub państw!")
