from Data import Data
from PyQt5.QtWidgets import QPushButton, QFileDialog
from reportlab.lib.utils import ImageReader
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from Graph import Graph, ReadData
from Exceptions import ErrorWindow


class PDFButton(QPushButton):
    __IMG_FORMAT = "png"

    def __init__(self):
        super().__init__("EXPORT TO PDF")
        self.__value = "EXPORT TO PDF"
        self.__pdf_generator = PdfReportGenerator()
        self.clicked.connect(self.__PDF)
        self.setStyleSheet("QPushButton"
                           "{"
                           "background-color : rgb(97,150,85);"
                           "}")

    def __PDF(self):
        try:
            data = ReadData(Data.FILENAME, Data.COUNTRIES_CLICKED, Data.START_DAY).get_data()
            plot = Graph(data, Data.START_DAY, "chorzy")

            img_data = plot.get_img()

            img = ImageReader(img_data)
            filename = self.__prepare_file_chooser()
            self.__pdf_generator.create_and_save_report(img, filename)
        except:
            ErrorWindow("Brak wykresu lub nazwy pliku!")

    def __prepare_file_chooser(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", filter="*.pdf")
        return filename


class PdfReportGenerator:

    def __init__(self):
        self.__author = "Nobody"
        self.__title = f"Covid report ({date.today()})"

    def create_and_save_report(self, img, filepath, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, img, pagesize)
        pdf_template.setAuthor(self.__author)
        pdf_template.setTitle(self.__title)
        pdf_template.save()

    def __create_pdf_template(self, filepath, img, pagesize):
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont("Helvetica", 24)
        title = "Raport Covid-19"

        title_x, title_y = A4[0] / 2, A4[1] - 40

        img_x, img_y = (A4[0]-560)/2, A4[1] - 500

        canvas.drawCentredString(title_x, title_y, title)
        canvas.setFont("Helvetica", 14)
        canvas.drawString(25, A4[1]-80, f"Zakres dat: od {Data.DAY} do {Data.END_DAY}.")
        canvas.drawImage(img, img_x, img_y, 560, 400)
        return canvas
