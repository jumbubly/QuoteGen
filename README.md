# Random Quote App

This is a simple application that generates random quotes and allows you to customize the display of the quotes. It uses the PyQt6 library for the graphical user interface and SQLite for data storage.

## Features

- Generate random quotes with author information.
- Translate quotes to different languages.
- Customize the font style and alignment of the quotes.
- Copy quotes to the clipboard.

## Requirements

- Python 3.x
- PyQt6 library
- SQLite

- pip install pyperclip
- pip install tempfile
- pip install pyttsx3
- pip install gtts
- pip install playsound
- pip install PyQt6
- pip install googletrans

## Installation

1. Clone the repository or download the source code files.

2. Install the required dependencies using pip:

3. Ensure that the `db.sqlite` file is present in the same directory as the `main.py` file. If not, create an empty SQLite database file named `db.sqlite`.

## Usage

To run the application, execute the following command:

- python main.py

The main window of the application will open, displaying a random quote and author information. You can click the "Generate" button to generate a new random quote.

### Customization Options

- **Font Style**: Use the "Select Font" button to choose a custom font for the quote display.

- **Text Style**: Select the desired text style (Normal, Italic, or Bold) from the corresponding drop-down menu.

- **Text Alignment**: Choose the alignment of the quote text (Left, Center, or Right) from the corresponding drop-down menu.

### Translation

You can select a language from the "Language" drop-down menu to translate the generated quote into that language. The translation is done using the Google Translate service.

### Copying Quotes

To copy a quote to the clipboard, click the "Copy" button. The quote will be copied in plain text format and can be pasted into other applications.

## Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please create a new issue or submit a pull request.

## License

This project has no licenese & is Copyright Protected By Github.
