from PyQt5.QtWidgets import QPushButton, QFileDialog
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from Graph import Graph, ReadData
from Exceptions import ErrorWindow
from Look_Config import Config


class PDFButton(QPushButton):
    __IMG_FORMAT = "png"

    def __init__(self, parent):
        super().__init__("EXPORT TO PDF")
        self.__parent = parent
        self.__value = "EXPORT TO PDF"
        self.__pdf_generator = PdfReportGenerator(parent)
        self.clicked.connect(self.__PDF)
        self.setStyleSheet(Config.PDF_BUTTON)

    def __PDF(self):
        try:
            data = ReadData(self.__parent.Data.FILENAME, self.__parent.Data.COUNTRIES_CLICKED,
                            self.__parent.Data.START_DAY, self.__parent.Data.END_DAY).get_data()
            plot = Graph(data, self.__parent.Data.START_DAY, self.__parent.Data.END_DAY,
                         self.__parent)
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

    def __init__(self, parent):
        self.__author = Config.TEMPLATE_AUTHOR
        self.__title = Config.TEMPLATE_TITLE
        self.__parent = parent

    def create_and_save_report(self, img, filepath, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, img, pagesize)
        pdf_template.setAuthor(self.__author)
        pdf_template.setTitle(self.__title)
        pdf_template.save()

    def __create_pdf_template(self, filepath, img, pagesize):
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont(Config.PDF_TITLE_FONT, 24)
        title = "Raport Covid-19"

        title_x, title_y = A4[0] / 2, A4[1] - 40

        img_x, img_y = (A4[0] - 560) / 2, A4[1] - 500

        canvas.drawCentredString(title_x, title_y, title)
        canvas.setFont(Config.PDF_STRING_FONT, 14)
        canvas.drawString(25, A4[1] - 80,
                          f"Zakres dat: od {self.__parent.Data.FIRST_PDF_DATE} do {self.__parent.Data.END_PDF_DATE}.")
        canvas.drawImage(img, img_x, img_y, 560, 400)
        return canvas
