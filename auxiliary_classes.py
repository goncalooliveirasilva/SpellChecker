from bloom_filter import BloomFilter
from PyQt6.QtGui import QKeySequence, QTextCharFormat, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, 
    QDialogButtonBox, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QWidget, 
    QListWidget, 
    QStackedWidget, 
    QListWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QKeySequenceEdit,
    QTextEdit
)


class SpellChecker:
    def __init__(self, words_file_path):
        self.bloom_filter = BloomFilter(100000, 3)
        self.load_words(words_file_path)

    def load_words(self, file):
        """Loads the dictionary words into the Bloom Filter"""
        try:
            with open(file, "r", encoding="utf-8") as f:
                for word in f:
                    self.bloom_filter.add(word.strip())
        except Exception as e:
            print(f"Error loading words into Bloom Filter: {e}")
    
    def check_word(self, word):
        """Checks if word exists in the dictionary (Bloom Filter)"""
        word = word.lower().strip()
        result = self.bloom_filter.member(word)
        print(f"Checking '{word}': {result}")
        return result


class UnsavedFileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Warning!")

        QBtn = (QDialogButtonBox.StandardButton.Discard | QDialogButtonBox.StandardButton.Cancel)

        self.buttonBox = QDialogButtonBox(QBtn)

        self.layout = QVBoxLayout()
        message = QLabel("Changes not saved. Do you want to continue?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Discard).clicked.connect(self.accept)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.reject)


class ConfWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Configurations")
        self.resize(600, 300)
        
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Sidebar menu
        self.menu = QListWidget()
        self.menu.setFixedWidth(150)
        self.menu.addItem("General")
        self.menu.addItem("Shortcuts")
        self.menu.addItem("Language")
        self.menu.addItem("Spell Checking")

        self.pages = QStackedWidget()
        self.general_page = QLabel("General Settings")
        self.shortcuts_page = QLabel("Shortcuts Settings")
        self.language_page = QLabel("Language Settings")
        self.spell_check_page = QLabel("Spell Checking Settings")

        self.pages.addWidget(self.general_page)
        self.pages.addWidget(self.shortcuts_page)
        self.pages.addWidget(self.language_page)
        self.pages.addWidget(self.spell_check_page)

        self.menu.currentRowChanged.connect(self.pages.setCurrentIndex)

        layout.addWidget(self.menu)
        layout.addWidget(self.pages)
