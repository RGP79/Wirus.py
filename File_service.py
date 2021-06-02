COUNTRY_COLUMN_ID = 1


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
        n_of_patients_in_time = [float(val) for val in n_of_patients_in_time]

        self.__vector = n_of_patients_in_time

    def get_vector(self):
        return self.__vector


class FirstDay:

    def __init__(self, filepath, parent):
        self.__filepath = filepath
        self.__parent = parent
        self.__get_day()

    def __get_day(self):
        with open(self.__filepath, "r") as f:
            line = f.readline()
            a = line.split(",")[4]
            b = a.split("/")
            if len(b[0]) == 1:
                self.__parent.Data.FIRST_DATE = f"20{b[2]}-0{b[0]}-{b[1]}"
            else:
                self.__parent.Data.FIRST_DATE = f"20{b[2]}-{b[0]}-{b[1]}"


class EndDay:

    def __init__(self, filepath, parent):
        self.__filepath = filepath
        self.__parent = parent
        self.__get_day()

    def __get_day(self):
        with open(self.__filepath, "r") as f:
            line = f.readline()
            data = line.split(",")
            a = data[-1]
            b = a.split("/")
            print(b)
            print(b[2][0:2])
            if len(b[0]) == 1:
                self.__parent.Data.LAST_DATE = f"20{b[2][0:2]}-0{b[0]}-{b[1]}"
            else:
                self.__parent.Data.LAST_DATE = f"20{b[2][0:2]}-{b[0]}-{b[1]}"


class ReadData:
    def __init__(self, filepath, countries, start_day, end_day):
        self.__data = dict()
        self.__read_countries_data(filepath, countries, start_day, end_day)

    def __read_countries_data(self, filepath, countries, start_day, end_day):
        countries_data = dict()

        with open(filepath, "r") as f:
            for line in f:
                if line[0] == ",":
                    maybe_country = line.split(",")[COUNTRY_COLUMN_ID]
                    if maybe_country in countries:
                        line = line.strip()
                        n_of_patients_in_time = PatientsVector(line).get_vector()

                        countries_data[maybe_country] = n_of_patients_in_time[start_day:end_day]

        self.__data = countries_data
        if len(countries) < 1:
            ghost_data = dict()
            ghost_data["Data"] = ["1"] * (end_day - start_day)
            self.__data = ghost_data

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
