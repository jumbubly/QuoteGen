import sys
import sqlite3
import random
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFontDialog, QGridLayout, QStyleFactory, QComboBox
from PyQt6.QtGui import QClipboard, QFont, QTextCursor, QColor, QAction
from googletrans import Translator

from quote import quote
from func import MenuManager

class QuoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Quote App")
        self.theme = "Light"  # Default theme
        self.language_combobox = QComboBox()
        self.populate_language_combobox()

        layout = QGridLayout()
        layout.addWidget(self.language_combobox, 5, 0, 1, 2)

        self.resize(800, 600)  # Set the window size

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f0f0f0;
            }

            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #dddddd;
                padding: 10px;
                font-family: Arial;
                font-size: 12pt;
                color: #333333;
            }

            QPushButton {
                background-color: #4d94ff;
                border: none;
                color: #ffffff;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #0073e6;
            }

            QPushButton:pressed {
                background-color: #003d99;
            }
            """
        )

        self.author_display = QTextEdit()
        self.author_display.setReadOnly(True)
        self.author_display.setFont(QFont("Arial", 12))
        self.author_display.setMaximumHeight(40)
        self.author_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.author_display.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.author_display.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.quote_display = QTextEdit()
        self.quote_display.setReadOnly(True)
        self.quote_display.setFont(QFont("Arial", 12))

        self.text_style_combobox = QComboBox()
        self.text_style_combobox.addItem("Normal")
        self.text_style_combobox.addItem("Italic")
        self.text_style_combobox.addItem("Bold")
        self.text_style_combobox.currentIndexChanged.connect(self.update_text_style)

        self.text_alignment_combobox = QComboBox()
        self.text_alignment_combobox.addItem("Left")
        self.text_alignment_combobox.addItem("Center")
        self.text_alignment_combobox.addItem("Right")
        self.text_alignment_combobox.currentIndexChanged.connect(self.update_text_alignment)

        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_quote)

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_quote)

        self.font_button = QPushButton("Select Font")
        self.font_button.clicked.connect(self.select_font)

        layout.addWidget(self.author_display, 0, 0, 1, 2)
        layout.addWidget(self.quote_display, 1, 0, 1, 2)
        layout.addWidget(self.text_style_combobox, 2, 0)
        layout.addWidget(self.text_alignment_combobox, 2, 1)
        layout.addWidget(self.generate_button, 3, 0)
        layout.addWidget(self.copy_button, 3, 1)
        layout.addWidget(self.font_button, 4, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect to the database
        self.connection = sqlite3.connect("db.sqlite")

        self.menu_manager = MenuManager(self)  # Instantiate MenuManager class and assign it to an instance variable

    def populate_language_combobox(self):
        languages = [
            "English",
            "Spanish",
            "Arabic",
            "Chinese (Simplified)",
            "Chinese (Traditional)",
            "Czech",
            "Danish",
            "Dutch",
            "French",
            "German",
            "Greek",
            "Hindi",
            "Hungarian",
            "Indonesian",
            "Italian",
            "Japanese",
            "Korean",
            "Norwegian",
            "Polish",
            "Portuguese",
            "Romanian",
            "Russian",
            "Slovak",
            "Swedish",
            "Thai",
            "Turkish",
            "Ukrainian",
            "Vietnamese",
            "Afrikaans",
            "Albanian",
            "Amharic",
            "Armenian",
            "Azerbaijani",
            "Basque",
            "Belarusian",
            "Bengali",
            "Bosnian",
            "Bulgarian",
            "Catalan",
            "Cebuano",
            "Chichewa",
            "Corsican",
            "Croatian",
            "Dutch",
            "Esperanto",
            "Estonian",
            "Filipino",
            "Finnish",
            "Frisian",
            "Galician",
            "Georgian",
            "Gujarati",
            "Haitian Creole",
            "Hausa",
            "Hawaiian",
            "Hebrew",
            "Hmong",
            "Icelandic",
            "Igbo",
            "Irish",
            "Javanese",
            "Kannada",
            "Kazakh",
            "Khmer",
            "Kurdish (Kurmanji)",
            "Kyrgyz",
            "Lao",
            "Latin",
            "Latvian",
            "Lithuanian",
            "Luxembourgish",
            "Macedonian",
            "Malagasy",
            "Malay",
            "Malayalam",
            "Maltese",
            "Maori",
            "Marathi",
            "Mongolian",
            "Myanmar (Burmese)",
            "Nepali",
            "Norwegian",
            "Odia",
            "Pashto",
            "Persian",
            "Polish",
            "Portuguese",
            "Punjabi",
            "Romanian",
            "Russian",
            "Samoan",
            "Scots Gaelic",
            "Serbian",
            "Sesotho",
            "Shona",
            "Sindhi",
            "Sinhala",
            "Slovak",
            "Slovenian",
            "Somali",
            "Spanish",
            "Sundanese",
            "Swahili",
            "Swedish",
            "Tajik",
            "Tamil",
            "Tatar",
            "Telugu",
            "Thai",
            "Turkish",
            "Turkmen",
            "Ukrainian",
            "Urdu",
            "Uyghur",
            "Uzbek",
            "Vietnamese",
            "Welsh",
            "Xhosa",
            "Yiddish",
            "Yoruba",
            "Zulu"
        ]
        self.language_combobox.addItems(languages)

    def get_author_details(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT Name, Profession FROM users")
        rows = cursor.fetchall()
        return [{"name": row[0], "profession": row[1]} for row in rows]

    def generate_quote(self):
        author_details = self.get_author_details()
        if author_details:
            author = random.choice(author_details)
            author_name = author["name"]
            profession = author["profession"]

            self.author_display.setPlainText(f"{author_name}, {profession}")
            self.author_display.setTextColor(QColor(0, 51, 153))  # Set author name color

            if profession is not None:
                # Generate quote using profession
                result = quote(profession, limit=2)
                random_quote = random.choice(result)
                quote_text = random_quote["quote"]
            else:
                # Generate quote without profession
                result = quote(author_name, limit=2)
                random_quote = random.choice(result)
                quote_text = random_quote["quote"]

            # Split quote into paragraphs
            paragraphs = quote_text.split("\n\n")
            formatted_quote = "\n\n".join(paragraphs)

            # Get the selected language from the combo box
            selected_language = self.language_combobox.currentText()

            # Translate the quote to the selected language
            translator = Translator()
            translation = translator.translate(formatted_quote, dest=selected_language)

            if translation.text:
                translated_quote = translation.text
                self.quote_display.setPlainText(translated_quote)
                self.update_text_alignment()
            else:
                QMessageBox.warning(self, "Translation Error", "Failed to translate the quote.")

    def copy_quote(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.quote_display.toPlainText())
        QMessageBox.information(self, "Quote Copied", "The quote has been copied to the clipboard.")

    def select_font(self):
        font, selected = QFontDialog.getFont()
        if selected:
            self.quote_display.setFont(font)

    def update_text_style(self):
        current_index = self.text_style_combobox.currentIndex()
        font = self.quote_display.font()
        if current_index == 0:
            font.setWeight(QFont.Weight.Normal)
            font.setStyle(QFont.Style.StyleNormal)
        elif current_index == 1:
            font.setWeight(QFont.Weight.Normal)
            font.setStyle(QFont.Style.StyleItalic)
        elif current_index == 2:
            font.setWeight(QFont.Weight.Bold)
            font.setStyle(QFont.Style.StyleNormal)
        self.quote_display.setFont(font)

    def update_text_alignment(self):
        current_index = self.text_alignment_combobox.currentIndex()
        if current_index == 0:
            self.quote_display.setAlignment(Qt.AlignmentFlag.AlignLeft)
        elif current_index == 1:
            self.quote_display.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        elif current_index == 2:
            self.quote_display.setAlignment(Qt.AlignmentFlag.AlignRight)

    def closeEvent(self, event):
        self.connection.close()  # Close the database connection before exiting
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    quote_app = QuoteApp()
    quote_app.show()
    sys.exit(app.exec())