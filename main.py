from PyQt6.QtWidgets import QApplication, QVBoxLayout, QComboBox, QLabel, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QToolBar, QStatusBar,QMessageBox
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3

class DatabaseConnection:
    def __init__(self,database_path='database.db'):
        self.database_path = database_path

    def connect(self):
        connection = sqlite3.connect(self.database_path)
        return connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(600,600)

        file_menu_item = self.menuBar().addMenu('&File')
        edit_menu_item = self.menuBar().addMenu('&Edit')
        help_menu_item = self.menuBar().addMenu('&Help')
        setting_menu_item = self.menuBar().addMenu('&Setting')

        add_student_action = QAction(QIcon('icons/add.png'),'Add Student',self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_action = QAction(QIcon('icons/search.png'),'Search', self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        about_action = QAction('About',self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        theme_action = QAction('Theme',self)
        setting_menu_item.addAction(theme_action)
        theme_action.triggered.connect(self.theme)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id','Name','Course','Number'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Add toolbar & toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Add status bar & status bar element
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell clicked
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton('Edit Record')
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton('Delete Record')
        delete_button.clicked.connect(self.delete)

        children =self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = DatabaseConnection().connect()
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def theme(self):
        dialog = ThemeDialog()
        dialog.exec()

class ThemeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Theme')
        self.setFixedWidth(150)

        layout = QGridLayout()

        light = QPushButton('Light')
        layout.addWidget(light,0,0)
        light.clicked.connect(self.light)

        dark = QPushButton('Dark')
        layout.addWidget(dark,1,0)
        dark.clicked.connect(self.dark)

        self.setLayout(layout)

    def light(self):
        light_stylesheet = """
        QWidget {
            background-color: #f5f5f5;
            color: #222;
        }
        QPushButton {
            border-radius: 20px;
            background-color: #e0e0e0;
            color: #222;
            border: 1px solid #bbb;
            padding: 5px;
            
        }
        QPushButton:pressed {
            background-color: #b3d7ff;
        }
        QLineEdit, QComboBox {
            background-color: #fff;
            color: #222;
            border: 1px solid #bbb;
        }
        QTableWidget {
            background-color: #fff;
            color: #222;
            gridline-color: #ccc;
        
        }
        QTableWidget::item:selected {
            background: #b3d7ff;
            color: #000;
        }
        QHeaderView::section {
            background-color: #e0e0e0;
            color: #222;
            border: 1px solid #bbb;
        }
        """

        app.setStyleSheet(light_stylesheet)
    def dark(self):
        dark_stylesheet = """
        QWidget {
            background-color: #2b2b2b;
            color: #f0f0f0;
        }
        QPushButton {
            border-radius: 20px;
            background-color: #3c3f41;
            color: #f0f0f0;
            border: 1px solid #555;
            padding: 5px;
        }
        QPushButton:pressed {
            border-radius: 20px;
            background-color: #b3d7ff;
            color: #000
        }
        QLineEdit, QComboBox {
            background-color: #232323;
            color: #f0f0f0;
            border: 1px solid #555;
        }
        """

        app.setStyleSheet(dark_stylesheet)

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')
        content = '''
        This app was created during the course "The Python Mega Course".
        Feel free to reuse or modify this app.
        Thanks for following. 😊😊😊
        '''
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Obtain Student name
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index,1).text()

        # Get student id
        self.student_id = main_window.table.item(index,0).text()

        # Add student name
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Add course combo box
        course = main_window.table.item(index,2).text()
        self.course_name = QComboBox()
        courses = ['Biology','Math','Astronomy','Physics']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course)
        layout.addWidget(self.course_name)

        # Add phone number
        phone_number = main_window.table.item(index,3).text()
        self.phone_number = QLineEdit(phone_number)
        self.phone_number.setPlaceholderText('Mobile')
        layout.addWidget(self.phone_number)

        # Add submit button
        submit_button = QPushButton('Register')
        submit_button.clicked.connect(self.update_data)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def update_data(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?',
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.phone_number.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        # Refresh data
        main_window.load_data()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Student Data')

        layout = QGridLayout()

        conformation = QLabel('Are you sure want to delete?')
        yes = QPushButton('Yes')
        yes.clicked.connect(self.delete_data)
        no = QPushButton('No')

        layout.addWidget(conformation,0,0,1,2)
        layout.addWidget(yes,1,0)
        layout.addWidget(no,1,1)
        self.setLayout(layout)


    def delete_data(self):

        # Get selected row's index & student id
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('DELETE from students WHERE id = ?',(student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()

        conformation_widget = QMessageBox()
        conformation_widget.setWindowTitle('Success!')
        conformation_widget.setText('The record was deleted successfully.')
        conformation_widget.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Add course combo box
        self.course_name = QComboBox()
        courses = ['Biology','Math','Astronomy','Physics']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add phone number
        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText('Mobile')
        layout.addWidget(self.phone_number)

        # Add submit button
        submit_button = QPushButton('Register')
        submit_button.clicked.connect(self.add_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)
    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.phone_number.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)',
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Search box
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText('Name')
        layout.addWidget(self.search_name)

        # Add button
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.name_search)
        layout.addWidget(search_button)

        self.setLayout(layout)


    def name_search(self):
        name = self.search_name.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name,Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(),1).setSelected(True)

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())