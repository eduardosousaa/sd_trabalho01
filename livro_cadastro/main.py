from login import LoginApp
import sys
from PyQt5.QtWidgets import QApplication
import firebase_admin
from firebase_admin import credentials

if __name__ == '__main__':
    # Inicializa o Firebase apenas uma vez
    cred = credentials.Certificate('firebase_config.json')
    firebase_admin.initialize_app(cred)

    app = QApplication(sys.argv)
    ex = LoginApp()
    ex.show()
    sys.exit(app.exec_())