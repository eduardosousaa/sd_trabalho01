from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox

class Ui_BookManager(object):
    def setupUi(self, BookManager):
        BookManager.setObjectName("BookManager")
        BookManager.resize(800, 600)
        BookManager.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #e0f7fa, stop:1 #80deea);
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLineEdit, QSpinBox {
                background-color: #ffffff;
                border: 1px solid #b0bec5;
                border-radius: 8px;
                padding: 8px;
                margin-bottom: 20px;
            }
            QPushButton {
                background-color: #00acc1;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #00838f;
            }
            QPushButton:pressed {
                background-color: #006064;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #b0bec5;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #00acc1;
                color: white;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)

        self.verticalLayout = QVBoxLayout(BookManager)
        self.formLayout = QFormLayout()
        self.inputTitle = QLineEdit(BookManager)
        self.inputAuthor = QLineEdit(BookManager)
        self.inputPages = QSpinBox(BookManager)
        self.inputPages.setMaximum(10000)
        self.inputYear = QSpinBox(BookManager)
        self.inputYear.setMinimum(1000)
        self.inputYear.setMaximum(2100)
        
        self.formLayout.addRow("Título do Livro:", self.inputTitle)
        self.formLayout.addRow("Autor Principal:", self.inputAuthor)
        self.formLayout.addRow("Quantidade de Páginas:", self.inputPages)
        self.formLayout.addRow("Ano de Publicação:", self.inputYear)
        self.verticalLayout.addLayout(self.formLayout)
        
        self.buttonLayout = QHBoxLayout()
        self.btnAdd = QPushButton("Adicionar", BookManager)
        self.btnUpdate = QPushButton("Atualizar", BookManager)
        self.btnDelete = QPushButton("Excluir", BookManager)
        self.btnClear = QPushButton("Limpar", BookManager)
        self.btnLogout = QPushButton("Logout", BookManager)
        self.btnLogout.setStyleSheet("""
                                     QPushButton {
                                        background-color: red; color: white;
                                     }
                                     
                                     QPushButton:hover {
                                        background-color: darkred;
                                    }""")
        
        self.buttonLayout.addWidget(self.btnAdd)
        self.buttonLayout.addWidget(self.btnUpdate)
        self.buttonLayout.addWidget(self.btnDelete)
        self.buttonLayout.addWidget(self.btnClear)
        self.buttonLayout.addWidget(self.btnLogout)  # Adding logout button to layout
        self.verticalLayout.addLayout(self.buttonLayout)
        
        self.tableBooks = QTableWidget(BookManager)
        self.tableBooks.setColumnCount(4)
        self.tableBooks.setHorizontalHeaderLabels(["Título", "Autor", "Páginas", "Ano"])
        self.verticalLayout.addWidget(self.tableBooks)

class MainWindow(QWidget, Ui_BookManager):
    def __init__(self, db, logout_callback):
        super().__init__()
        self.db = db
        self.logout_callback = logout_callback
        self.setupUi(self)
        self.btnAdd.clicked.connect(self.add_book)
        self.btnUpdate.clicked.connect(self.update_book)
        self.btnDelete.clicked.connect(self.delete_book)
        self.btnClear.clicked.connect(self.clear_fields)
        self.btnLogout.clicked.connect(self.logout_callback)  # Connect logout button to the callback
        self.tableBooks.cellClicked.connect(self.load_selected_book)
        self.load_books()

    def add_book(self):
        book = {
            'titulo': self.inputTitle.text(),
            'autor': self.inputAuthor.text(),
            'paginas': self.inputPages.value(),
            'ano': self.inputYear.value()
        }
        if book['titulo']:
            self.db.collection('livros').document(book['titulo']).set(book)
            self.load_books()
            self.clear_fields()
            QMessageBox.information(self, "Sucesso", "Livro adicionado com sucesso!")

    def update_book(self):
        title = self.inputTitle.text()
        if title:
            book = {
                'titulo': title,
                'autor': self.inputAuthor.text(),
                'paginas': self.inputPages.value(),
                'ano': self.inputYear.value()
            }
            self.db.collection('livros').document(title).update(book)
            self.load_books()
            QMessageBox.information(self, "Sucesso", "Livro atualizado com sucesso!")

    def delete_book(self):
        title = self.inputTitle.text()
        if title:
            self.db.collection('livros').document(title).delete()
            self.load_books()
            self.clear_fields()
            QMessageBox.information(self, "Sucesso", "Livro excluído com sucesso!")

    def load_books(self):
        self.tableBooks.setRowCount(0)
        books = self.db.collection('livros').stream()
        for idx, book in enumerate(books):
            data = book.to_dict()
            self.tableBooks.insertRow(idx)
            self.tableBooks.setItem(idx, 0, QTableWidgetItem(data['titulo']))
            self.tableBooks.setItem(idx, 1, QTableWidgetItem(data['autor']))
            self.tableBooks.setItem(idx, 2, QTableWidgetItem(str(data['paginas'])))
            self.tableBooks.setItem(idx, 3, QTableWidgetItem(str(data['ano'])))

    def clear_fields(self):
        self.inputTitle.clear()
        self.inputAuthor.clear()
        self.inputPages.setValue(0)
        self.inputYear.setValue(1000)

    def load_selected_book(self, row, column):
        self.inputTitle.setText(self.tableBooks.item(row, 0).text())
        self.inputAuthor.setText(self.tableBooks.item(row, 1).text())
        self.inputPages.setValue(int(self.tableBooks.item(row, 2).text()))
        self.inputYear.setValue(int(self.tableBooks.item(row, 3).text()))
