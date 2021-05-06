class TooMuchCountriesError(Exception):
    # za duzo wybranych panstw error
    def __init__(self):
        msg = f"Error! "
        super().__init__(msg)


class FileError(Exception):
    # plik nie istnieje lub ma zly format
    def __init__(self, arg_name):
        msg = f"Error! Cannot load a file. There is no such file as {arg_name}."
        super().__init__(msg)


class PDFError(Exception):
    # nie ma wczytanych danych lub wykresu do pdfa
    def __init__(self):
        msg = f"Error! Not enough data to make a file."
        super().__init__(msg)


class NoCountriesError(Exception):
    #gdy nie ma zadnego wybranego kraju i wciskasz rob wykres
    def __init__(self):
        msg = f"Error! "
        super().__init__(msg)
