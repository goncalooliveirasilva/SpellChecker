import json
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt
import os
from auxiliary_classes import UnsavedFileDialog
from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QTextEdit,
    QToolBar,
    QFileDialog,
    QTabWidget,
    QMenuBar,
    QMessageBox,
    QDialog
)

SESSION_FILE = "session.json"
SUPPORTED_FILES = """
                    Text Files (*.txt *.md *.log *.cfg *.ini);;
                    Python Files (*.py);;
                    C/C++ Files (*.c *.cpp *.h *.hpp);;
                    Java Files (*.java);;
                    JavaScript Files (*.js *.ts);;
                    HTML/CSS Files (*.html *.css);;
                    All Files (*)
                """

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.resize(800, 500)
        #self.setWindowIcon(QIcon())

        self.open_files = {} # store open files: {tab_index: file_path}

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabBar().tabMoved.connect(self.update_tab_order)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tabs)

        # Toolbar
        self.toolbar = QToolBar("Options")
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("&File")
        self.conf_menu = self.menu.addMenu("&Configurations")

        # Actions
        self.new_file_action = QAction("New File", self)
        self.new_file_action.setShortcut(QKeySequence("Ctrl+N"))
        self.new_file_action.triggered.connect(self.new_file)

        self.open_file_action = QAction("Open File", self)
        self.open_file_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_file_action.triggered.connect(self.open_file)

        self.save_file_action = QAction("Save File", self)
        self.save_file_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_file_action.triggered.connect(self.save_file)

        self.save_all_action = QAction("Save All", self)
        self.save_all_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.save_all_action.triggered.connect(self.save_all_files)

        self.edit_shortcuts_action = QAction("Edit Shortcuts", self)
        #self.edit_shortcuts_action.triggered.connect()

        self.toolbar.addAction(self.new_file_action)
        self.toolbar.addAction(self.open_file_action)
        self.toolbar.addAction(self.save_file_action)
        self.toolbar.addAction(self.save_all_action)
        self.toolbar.addAction(self.edit_shortcuts_action)

        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.save_file_action)
        self.file_menu.addAction(self.save_all_action)

        self.conf_menu.addAction(self.edit_shortcuts_action)


        self.restore_session()

        if self.tabs.count() == 0:
            self.new_file() # start with an empty tab


    def new_file(self):
        """Create a new tab with an empty text edit"""
        text_edit = QTextEdit()
        index = self.tabs.addTab(text_edit, "Untitled") # add a new tab
        self.tabs.setCurrentIndex(index) # switch to the new tab
        self.open_files[index] = None
        self.track_file_changes(text_edit)


    def open_file(self):
        """Opens a file and adds it's content to a new tab"""
        home_dir = os.path.expanduser("~")
        file_names, _ = QFileDialog.getOpenFileNames(self, "Open File", home_dir, SUPPORTED_FILES)

        for file_name in file_names:
            if file_name:
                try:
                    # Check if the file is already open
                    for idx, path in self.open_files.items():
                        if path == file_name:
                            self.tabs.setCurrentIndex(idx)
                            return
                
                    with open(file_name, "r", encoding="utf-8") as file:
                        text = file.read()    
    
                    # Create new tab for the file
                    text_edit = QTextEdit()
                    text_edit.setPlainText(text)
                    index = self.tabs.addTab(text_edit, os.path.basename(file_name))
                    self.tabs.setCurrentIndex(index)
                    self.open_files[index] = file_name

                    self.track_file_changes(text_edit)

                except Exception as e:
                    print(f"Error opening file: {e}")


    def save_file(self):
        """Saves the current file"""
        index = self.tabs.currentIndex()
        if index == -1:
            return
        
        file_name = self.open_files.get(index)

        # If it's a new file
        if file_name is None:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", os.path.expanduser("~"), SUPPORTED_FILES)
            if not file_name:
                return
            
            self.open_files[index] = file_name
            self.tabs.setTabText(index, os.path.basename(file_name))

        # Save
        try:
            text_edit = self.tabs.widget(index)
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(text_edit.toPlainText())
            self.tabs.setTabText(index, os.path.basename(file_name)) # Remove "*"

        except Exception as e:
            QMessageBox.critical(self, f"Error saving file: {e}")


    def save_all_files(self):
        """Saves all opened files"""
        for index, file_name in self.open_files.items():
            if file_name:
                try:
                    text_edit = self.tabs.widget(index)
                    with open(file_name, "w", encoding="utf-8") as file:
                        file.write(text_edit.toPlainText())
                    self.tabs.setTabText(index, os.path.basename(file_name)) # Remove "*"
                except Exception as e:
                    QMessageBox.critical(self, f"Error saving file: {e}")
    

    def close_tab(self, index):
        """Closes the selected tab and updates session file"""
        if index in self.open_files:
            del self.open_files[index]
        self.tabs.removeTab(index)
        if self.tabs.count() == 0:
            self.new_file()
        self.save_session()


    def closeEvent(self, event):
        """Saves session on close and check for unsaved files"""
        if self.has_unsaved_files():
            dialog = UnsavedFileDialog(self)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                event.accept()
            else:
                event.ignore()
        else:
            self.save_session()
            event.accept()

    
    def has_unsaved_files(self):
        """Launches a pop up if any file has not been saved"""
        num_tabs = self.tabs.count()
        for index in range(num_tabs):
            if self.tabs.tabText(index).startswith("*"):
                return True
        return False
    

    def save_session(self):
        """Saves the names of the currently opened files before closing"""
        open_files = {i: path for i, path in self.open_files.items() if path}

        if open_files:
            with open(SESSION_FILE, "w") as file:
                json.dump(open_files, file)
        else:
            if os.path.exists(SESSION_FILE):
                os.remove(SESSION_FILE)


    def restore_session(self):
        """Restores previously opened files"""
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r") as file:
                    open_files = json.load(file)
                
                for _, file_path in open_files.items():
                    if os.path.exists(file_path):
                        self.open_file_from_path(file_path)
            except Exception as e:
                print(f"Error restoring session: {e}")
    

    def open_file_from_path(self, file_path):
        """Opens a file from a known path (session restore)"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
            
            text_edit = QTextEdit()
            text_edit.setPlainText(text)

            index = self.tabs.addTab(text_edit, os.path.basename(file_path))
            self.tabs.setCurrentIndex(index)
            self.open_files[index] = file_path

            self.track_file_changes(text_edit)

        except Exception as e:
            print(f"Error opening file: {e}")


    def mark_file_as_unsaved(self, text_edit):
        """Marks a tab name as unsaved"""
        index = self.tabs.indexOf(text_edit)
        if index != -1:
            tab_title = self.tabs.tabText(index)
            if not tab_title.startswith("*"):
                self.tabs.setTabText(index, f"*{tab_title}")


    def track_file_changes(self, text_edit):
        """Connects text edit changes to track modifications"""
        text_edit.textChanged.connect(lambda: self.mark_file_as_unsaved(text_edit))


    def update_tab_order(self, to_index, from_index):
        """Rearrange open_files dictionary when tabs are moved"""
        keys = list(self.open_files.keys())
        values = list(self.open_files.values())

        values.insert(to_index, values.pop(from_index))
        self.open_files = dict(zip(keys, values))