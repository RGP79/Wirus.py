from datetime import date


class Config:
    INPUT_BTN = "QPushButton" \
                "{" \
                "background-color : rgb(97,150,85);" \
                "}"
    BACKGROUND_COLOR = "QWidget" \
                       "{" \
                       "background-color : grey;" \
                       "}"
    RESET_BTN = "QPushButton" \
                "{" \
                "background-color : rgb(97,150,85);" \
                "}"
    SEARCH_LINE = "QLineEdit" \
                  "{" \
                  "background-color : lightblue;" \
                  "}"
    PDF_BUTTON = "QPushButton" \
                 "{" \
                 "background-color : rgb(97,150,85);" \
                 "}"
    SLIDER = "selection-color : rgb(196,245,95);"
    COUNTRY_BTN_UNCLICKED = "QPushButton" \
                            "{" \
                            "background-color : lightblue;" \
                            "}"
    COUNTRY_BTN_CLICKED = "QPushButton" \
                          "{" \
                          "background-color : rgb(97,150,85);" \
                          "}"
    WINDOW_STYLE = 'Oxygen'
    PDF_TITLE_FONT = "Helvetica"
    PDF_STRING_FONT = "Helvetica"
    TEMPLATE_AUTHOR = "Nobody"
    TEMPLATE_TITLE = f"Covid report generated ({date.today()})"
