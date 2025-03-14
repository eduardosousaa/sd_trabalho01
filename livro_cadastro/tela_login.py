from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox

class Ui_LoginScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setupUi(self)

    def setupUi(self, LoginScreen):
        LoginScreen.setObjectName("LoginScreen")
        LoginScreen.resize(400, 300)
        LoginScreen.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #e0f7fa, stop:1 #80deea);
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLabel {
                color: #37474f;
                font-weight: 600;
                margin-bottom: 6px;
            }
            QLineEdit {
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
        """)

        self.verticalLayout = QVBoxLayout(LoginScreen)
        self.formLayout = QFormLayout()

        self.labelEmail = QLabel("Email:")
        self.inputEmail = QLineEdit()
        self.formLayout.addRow(self.labelEmail, self.inputEmail)

        self.labelPassword = QLabel("Senha:")
        self.inputPassword = QLineEdit()
        self.inputPassword.setEchoMode(QLineEdit.Password)
        self.formLayout.addRow(self.labelPassword, self.inputPassword)

        self.verticalLayout.addLayout(self.formLayout)

        self.btnEnter = QPushButton("Entrar")
        self.verticalLayout.addWidget(self.btnEnter, alignment=QtCore.Qt.AlignCenter)

        self.btnRegister = QPushButton("Cadastrar")
        self.verticalLayout.addWidget(self.btnRegister, alignment=QtCore.Qt.AlignCenter)

        self.btnEnter.clicked.connect(self.attempt_login)
        self.btnRegister.clicked.connect(self.register)

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def register(self):
        email = self.inputEmail.text()
        password = self.inputPassword.text()
        if email and password:
            user_ref = self.db.collection('users').document(email)
            if user_ref.get().exists:
                self.show_message("Erro", "Usuário já cadastrado.")
            else:
                user_ref.set({'email': email, 'password': password})
                self.show_message("Sucesso", "Usuário cadastrado com sucesso!")
        else:
            self.show_message("Erro", "Por favor, preencha todos os campos.")

    def attempt_login(self):
        email = self.inputEmail.text()
        password = self.inputPassword.text()
        self.login(email, password)  # Chama a função de login com argumentos

    def login(self, email, password):
        user_ref = self.db.collection('users').document(email).get()
        if user_ref.exists and user_ref.to_dict().get('password') == password:
            # self.show_message("Sucesso", "Login realizado com sucesso!")
            return True
        else:
            self.show_message("Erro", "Email ou senha incorretos.")
            return False
