import pyperclip
import tempfile
import pyttsx3
from gtts import gTTS
from playsound import playsound
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction, QDesktopServices, QClipboard, QPalette, QColor, QBrush
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton, QMessageBox, QColorDialog, QFileDialog

class MenuManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.create_menus()

    def create_menus(self):
        menubar = self.main_window.menuBar()

        file_menu = menubar.addMenu("Open")
        options_menu = menubar.addMenu("Options")
        about_menu = menubar.addMenu("Help")

        open_action = QAction("Open File", self.main_window)
        options_action = QAction("Themes", self.main_window)
        download_audio_action = QAction("Download Audio", self.main_window)
        self.about_action = QAction("About", self.main_window)

        options_action.triggered.connect(self.open_theme_dialog)
        download_audio_action.triggered.connect(self.open_audio_dialog)
        self.about_action.triggered.connect(self.show_about_info)

        file_menu.addAction(open_action)
        options_menu.addAction(options_action)
        options_menu.addAction(download_audio_action)  # Add this line
        about_menu.addAction(self.about_action)

    def open_theme_dialog(self):
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("Themes")

        layout = QVBoxLayout()

        themes = ["Light", "Dark", "Sky Blue", "Green", "Purple"]
        for theme in themes:
            button = QPushButton(theme)
            button.clicked.connect(lambda checked, theme=theme: self.set_theme(theme))
            layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec()

    def open_audio_dialog(self):
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("Download Audio")

        layout = QVBoxLayout()

        voice_label = QLabel("Select voice:")
        layout.addWidget(voice_label)

        voice_male_button = QPushButton("Male")
        voice_male_button.clicked.connect(lambda: self.download_audio("male"))
        layout.addWidget(voice_male_button)

        voice_female_button = QPushButton("Female")
        voice_female_button.clicked.connect(lambda: self.download_audio("female"))
        layout.addWidget(voice_female_button)

        dialog.setLayout(layout)
        dialog.exec()

    def download_audio(self, voice):
        text = self.main_window.quote_display.toPlainText()  # Get the text from the quote display

        if voice == "male":
            engine = pyttsx3.init()
            engine.save_to_file(text, "male_voice.mp3")
            engine.runAndWait()
            playsound("male_voice.mp3")
        elif voice == "female":
            tts = gTTS(
                text=text,
                lang="en",
                slow=False,
                tld="com",
                lang_check=False,
                pre_processor_funcs=[lambda x: x.replace("\n", " ")],
            )

            file_dialog = QFileDialog(self.main_window)
            file_dialog.setNameFilter("MP3 files (*.mp3)")
            file_dialog.setDefaultSuffix("mp3")
            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                selected_file = file_dialog.selectedFiles()[0]
                tts.save(selected_file)
                playsound(selected_file)

    def set_theme(self, theme):
        self.main_window.theme = theme

        if theme == "Light":
            self.set_light_theme()
        elif theme == "Dark":
            self.set_dark_theme()
        elif theme == "Sky Blue":
            self.set_sky_blue_theme()
        elif theme == "Green":
            self.set_green_theme()
        elif theme == "Purple":
            self.set_purple_theme()

    def set_light_theme(self):
        self.main_window.setStyleSheet(
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

    def set_dark_theme(self):
        self.main_window.setStyleSheet(
            """
            QMainWindow {
                background-color: #333333;
            }

            QTextEdit {
                background-color: #1a1a1a;
                border: 1px solid #555555;
                padding: 10px;
                font-family: Arial;
                font-size: 12pt;
                color: #ffffff;
            }

            QPushButton {
                background-color: #555555;
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

    def set_sky_blue_theme(self):
        self.main_window.setStyleSheet(
            """
            QMainWindow {
                background-color: #b3e6ff;
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
                background-color: #b3f6ff;
                border: none;
                color: #000000;
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

    def set_green_theme(self):
        self.main_window.setStyleSheet(
            """
            QMainWindow {
                background-color: #c1e5be;
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
                background-color: #55a630;
                border: none;
                color: #ffffff;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #207d09;
            }

            QPushButton:pressed {
                background-color: #135705;
            }
            """
        )

    def set_purple_theme(self):
        self.main_window.setStyleSheet(
            """
            QMainWindow {
                background-color: #e5d2e2;
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
                background-color: #7a4eb1;
                border: none;
                color: #ffffff;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #5f2992;
            }

            QPushButton:pressed {
                background-color: #431e68;
            }
            """
        )

    def show_about_info(self):
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("About")

        layout = QVBoxLayout()

        author_label = QLabel("Author: ReKingg")
        layout.addWidget(author_label)

        github_button = QPushButton("GitHub Account")
        github_button.clicked.connect(lambda: self.open_link_in_browser("https://github.com/jumbubly"))
        layout.addWidget(github_button)

        cracked_button = QPushButton("Cracked Account")
        cracked_button.clicked.connect(lambda: self.open_link_in_browser("https://cracked.io/rekingg"))
        layout.addWidget(cracked_button)

        bitcoin_label = QLabel("<b>Bitcoin Code: bc1qadtnnc06hg3ekck785xxw4pmv89nfd2p5q7v3n</b>")
        layout.addWidget(bitcoin_label)

        copy_button = QPushButton("Copy to Clipboard")
        copy_button.clicked.connect(self.copy_bitcoin_address)
        layout.addWidget(copy_button)

        dialog.setLayout(layout)
        dialog.exec()

    def copy_bitcoin_address(self):
        bitcoin_code = "bc1qadtnnc06hg3ekck785xxw4pmv89nfd2p5q7v3n"
        pyperclip.copy(bitcoin_code)
        QMessageBox.information(None, "Copied", "Bitcoin address copied to clipboard.")

    def open_link_in_browser(self, url):
        QDesktopServices.openUrl(QUrl(url))
