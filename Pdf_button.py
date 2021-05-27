from io import BytesIO

from Wirus.Data import Data
from PyQt5.QtWidgets import QPushButton, QFileDialog
from reportlab.lib.utils import ImageReader
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

from Wirus.Graph import Graph, ReadData


class PDFButton(QPushButton):
    __IMG_FORMAT = "png"

    # implementacja przycsiku do tworzenia pdf
    def __init__(self):
        super().__init__("EXPORT TO PDF")
        self.__value = "EXPORT TO PDF"
        self.__pdf_generator = PdfReportGenerator()
        self.clicked.connect(self.__PDF)
        self.setStyleSheet("QPushButton"
                           "{"
                           "background-color : rgb(196,245,95);"
                           "}")

    def __PDF(self):
        data = ReadData(Data.FILENAME, Data.COUNTRIES_CLICKED, Data.START_DAY).get_data()
        plot = Graph(data, Data.START_DAY, "chorzy")

        img_data = plot.get_img()

        img = ImageReader(img_data)
        filename = self.__prepare_file_chooser()
        print(filename)
        self.__pdf_generator.create_and_save_report(img, filename)
        print("finish")

    def __prepare_file_chooser(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF report", filter="All Files (*)")
        return filename


class PdfReportGenerator:

    def __init__(self):
        self.__author = "Nobody"
        self.__title = f"Sin(x) report ({date.today()})"

    def create_and_save_report(self, img, filepath, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, img, pagesize)
        pdf_template.setAuthor(self.__author)
        pdf_template.setTitle(self.__title)
        pdf_template.save()

    def __create_pdf_template(self, filepath, img, pagesize):
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont("Times-Roman", 40)
        title = "Wykresik"
        title_magic_offset, img_magic_offset = 100, 600
        title_x, title_y = A4[0] / 2, A4[1] - title_magic_offset
        img_x, img_y = 0, A4[1] - img_magic_offset

        canvas.drawCentredString(title_x, title_y, title)
        canvas.drawImage(img, img_x, img_y, 560, 400)
        canvas.drawString(1, 1, "lewap chuju")
        return canvas
