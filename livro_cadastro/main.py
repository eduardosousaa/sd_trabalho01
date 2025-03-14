import sys
import firebase_admin
from firebase_admin import credentials, firestore
from PyQt5.QtWidgets import QApplication, QWidget
from tela_adm import MainWindow  # Importando a classe MainWindow de tela_adm.py
from tela_login import Ui_LoginScreen  # Importando a classe Ui_LoginScreen de tela_login.py

def init_firebase():
    # Inicializa o Firebase apenas uma vez, se ainda não foi inicializado
    if not firebase_admin._apps:
        cred = credentials.Certificate('firebase_config.json')
        firebase_admin.initialize_app(cred)
    return firestore.client()

class AppManager(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.loginScreen = QWidget()
        self.uiLogin = Ui_LoginScreen(self.db)
        self.uiLogin.setupUi(self.loginScreen)
        self.loginScreen.show()
        self.uiLogin.btnEnter.clicked.connect(self.login_success)

    def login_success(self):
        if self.uiLogin.login(self.uiLogin.inputEmail.text(), self.uiLogin.inputPassword.text()):
            self.loginScreen.hide()
            self.bookManagerWindow = MainWindow(self.db, self.handle_logout)
            self.bookManagerWindow.show()

    def handle_logout(self):
        self.bookManagerWindow.close()
        self.loginScreen.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = init_firebase()
    ex = AppManager(db)
    sys.exit(app.exec_())

