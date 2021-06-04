class Data:
    def __init__(self):
        self.__countries_clicked = []
        self.__filename = None
        self.__start_day = 0
        self.__end_day = 10
        self.__first_date = None
        self.__last_date = None
        self.__start_pdf_date = None
        self.__end_pdf_date = None
        self.__check_box = "Semilogy"

    def add_country(self, new):
        self.__countries_clicked.append(new)

    def remove_country(self, old):
        self.__countries_clicked.remove(old)

    def reset_countries(self):
        self.__countries_clicked = []

    def get_countries(self):
        return self.__countries_clicked

    def set_filename(self, new):
        self.__filename = new

    def get_filename(self):
        return self.__filename

    def set_start_day(self, new):
        self.__start_day = new

    def get_start_day(self):
        return self.__start_day

    def set_end_day(self, new):
        self.__end_day = new

    def get_end_day(self):
        return self.__end_day

    def set_first_date(self, new):
        self.__first_date = new

    def get_first_date(self):
        return self.__first_date

    def set_last_date(self, new):
        self.__last_date = new

    def get_last_date(self):
        return self.__last_date

    def set_start_pdf_date(self, new):
        self.__start_pdf_date = new

    def get_start_pdf_date(self):
        return self.__start_pdf_date

    def set_end_pdf_date(self, new):
        self.__end_pdf_date = new

    def get_end_pdf_date(self):
        return self.__end_pdf_date

    def set_check_box(self, new):
        self.__check_box = new

    def get_check_box(self):
        return self.__check_box
