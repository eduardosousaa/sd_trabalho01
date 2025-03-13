from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import sys
from firebase_admin import firestore
import requests
from ui import LivroCadastroApp

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = firestore.client()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Email')
        layout.addWidget(self.email_input)

        self.senha_input = QLineEdit(self)
        self.senha_input.setPlaceholderText('Senha')
        self.senha_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.senha_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.fazer_login)
        layout.addWidget(self.login_button)

        self.cadastrar_button = QPushButton('Cadastrar', self)
        self.cadastrar_button.clicked.connect(self.ir_para_cadastro)
        layout.addWidget(self.cadastrar_button)

        self.setLayout(layout)

    def fazer_login(self):
        email = self.email_input.text()
        senha = self.senha_input.text()

        # URL da API de login do Firebase
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyCOicSOtOwElbdxU4rTZPBRRrlZQ2q4s_0"

        # Dados para enviar na requisição
        data = {
            "email": email,
            "password": senha,
            "returnSecureToken": True
        }

        try:
            # Faz a requisição POST para autenticar o usuário
            response = requests.post(url, json=data)
            result = response.json()

            if "error" in result:
                QMessageBox.warning(self, 'Erro', 'Email ou senha incorretos!')
            else:
                QMessageBox.information(self, 'Sucesso', 'Login realizado com sucesso!')
                self.ir_para_gerenciamento_livros()
        except Exception as e:
            QMessageBox.warning(self, 'Erro', f'Erro ao fazer login: {str(e)}')

    def ir_para_cadastro(self):
        self.cadastro_window = CadastroApp(self.db)  # Passa o Firestore para a tela de cadastro
        self.cadastro_window.show()
        self.hide()

    def ir_para_gerenciamento_livros(self):
        self.gerenciamento_window = LivroCadastroApp(self.db)  # Passa o Firestore para a tela de livros
        self.gerenciamento_window.show()
        self.hide()

class CadastroApp(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cadastro')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Email')
        layout.addWidget(self.email_input)

        self.senha_input = QLineEdit(self)
        self.senha_input.setPlaceholderText('Senha')
        self.senha_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.senha_input)

        self.cadastrar_button = QPushButton('Cadastrar', self)
        self.cadastrar_button.clicked.connect(self.fazer_cadastro)
        layout.addWidget(self.cadastrar_button)

        self.setLayout(layout)

    def fazer_cadastro(self):
        email = self.email_input.text()
        senha = self.senha_input.text()

        # URL da API de cadastro do Firebase
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyCOicSOtOwElbdxU4rTZPBRRrlZQ2q4s_0"

        # Dados para enviar na requisição
        data = {
            "email": email,
            "password": senha,
            "returnSecureToken": True
        }

        try:
            # Faz a requisição POST para cadastrar o usuário
            response = requests.post(url, json=data)
            result = response.json()

            if "error" in result:
                QMessageBox.warning(self, 'Erro', f'Erro ao cadastrar: {result["error"]["message"]}')
            else:
                QMessageBox.information(self, 'Sucesso', 'Cadastro realizado com sucesso!')
                self.ir_para_gerenciamento_livros()
        except Exception as e:
            QMessageBox.warning(self, 'Erro', f'Erro ao cadastrar: {str(e)}')

    def ir_para_gerenciamento_livros(self):
        self.gerenciamento_window = LivroCadastroApp(self.db)  # Passa o Firestore para a tela de livros
        self.gerenciamento_window.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginApp()
    ex.show()
    sys.exit(app.exec_())