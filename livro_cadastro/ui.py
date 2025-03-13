from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import sys

import firebase_admin

class LivroCadastroApp(QWidget):
    def __init__(self, db):  # Agora aceita o Firestore como argumento
        super().__init__()
        self.db = db  # Guarda a conexão com o Firestore
        self.initUI()  # Inicializa a interface

    def initUI(self):
        self.setWindowTitle('Cadastro de Livros')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Campos de entrada
        self.titulo_input = QLineEdit(self)
        self.titulo_input.setPlaceholderText('Título do Livro')
        layout.addWidget(self.titulo_input)

        self.autor_input = QLineEdit(self)
        self.autor_input.setPlaceholderText('Autor Principal')
        layout.addWidget(self.autor_input)

        self.paginas_input = QLineEdit(self)
        self.paginas_input.setPlaceholderText('Quantidade de Páginas')
        layout.addWidget(self.paginas_input)

        self.ano_input = QLineEdit(self)
        self.ano_input.setPlaceholderText('Ano de Publicação')
        layout.addWidget(self.ano_input)

        # Botões
        self.add_button = QPushButton('Adicionar Livro', self)
        self.add_button.clicked.connect(self.adicionar_livro)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton('Atualizar Livro', self)
        self.update_button.clicked.connect(self.atualizar_livro)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton('Deletar Livro', self)
        self.delete_button.clicked.connect(self.deletar_livro)
        layout.addWidget(self.delete_button)
        
        # Botão de logout
        self.logout_button = QPushButton('Logout', self)
        self.logout_button.setStyleSheet("background-color: red; color: white;")
        self.logout_button.clicked.connect(self.fazer_logout)
        layout.addWidget(self.logout_button)

        # Tabela para exibir os livros
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)  # 5 colunas: Título, Autor, Páginas, Ano, ID (oculto)
        self.table.setHorizontalHeaderLabels(['Título', 'Autor', 'Páginas', 'Ano', 'ID'])
        self.table.setColumnHidden(4, True)  # Oculta a coluna do ID
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Selecionar linha inteira
        self.table.cellClicked.connect(self.selecionar_livro)  # Preencher campos ao selecionar
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.carregar_livros()  # Carrega os livros ao iniciar
    
    def fazer_logout(self):
        from login import LoginApp  # Importação dentro da função para evitar ciclo

        QMessageBox.information(self, 'Logout', 'Você saiu da conta!')
        self.close()  # Fecha a janela atual
        self.login_window = LoginApp()  # Cria uma nova tela de login
        self.login_window.show()  # Exibe a tela de login

    def adicionar_livro(self):
        titulo = self.titulo_input.text()
        autor = self.autor_input.text()
        paginas = self.paginas_input.text()
        ano = self.ano_input.text()

        if titulo and autor and paginas and ano:
            livro = {
                'titulo': titulo,
                'autor': autor,
                'paginas': paginas,
                'ano': ano
            }
            self.db.collection('livros').add(livro)
            QMessageBox.information(self, 'Sucesso', 'Livro adicionado com sucesso!')
            self.carregar_livros()  # Recarrega a lista de livros após adicionar
        else:
            QMessageBox.warning(self, 'Erro', 'Todos os campos são obrigatórios!')

    def carregar_livros(self):
        self.table.setRowCount(0)  # Limpa a tabela antes de carregar os dados
        livros = self.db.collection('livros').stream()  # Acessa o Firestore
        for livro in livros:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(livro.to_dict()['titulo']))
            self.table.setItem(row_position, 1, QTableWidgetItem(livro.to_dict()['autor']))
            self.table.setItem(row_position, 2, QTableWidgetItem(livro.to_dict()['paginas']))
            self.table.setItem(row_position, 3, QTableWidgetItem(livro.to_dict()['ano']))
            self.table.setItem(row_position, 4, QTableWidgetItem(livro.id))  # Armazena o ID na coluna oculta

    def selecionar_livro(self, row):
        # Preenche os campos com os dados do livro selecionado
        self.titulo_input.setText(self.table.item(row, 0).text())
        self.autor_input.setText(self.table.item(row, 1).text())
        self.paginas_input.setText(self.table.item(row, 2).text())
        self.ano_input.setText(self.table.item(row, 3).text())

    def atualizar_livro(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            livro_id = self.table.item(selected_row, 4).text()  # Obtém o ID do livro
            titulo = self.titulo_input.text()
            autor = self.autor_input.text()
            paginas = self.paginas_input.text()
            ano = self.ano_input.text()

            if titulo and autor and paginas and ano:
                livro = {
                    'titulo': titulo,
                    'autor': autor,
                    'paginas': paginas,
                    'ano': ano
                }
                self.db.collection('livros').document(livro_id).update(livro)
                QMessageBox.information(self, 'Sucesso', 'Livro atualizado com sucesso!')
                self.carregar_livros()  # Recarrega a lista de livros após atualizar
            else:
                QMessageBox.warning(self, 'Erro', 'Todos os campos são obrigatórios!')
        else:
            QMessageBox.warning(self, 'Erro', 'Selecione um livro para atualizar!')

    def deletar_livro(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            livro_id = self.table.item(selected_row, 4).text()  # Obtém o ID do livro
            self.db.collection('livros').document(livro_id).delete()
            QMessageBox.information(self, 'Sucesso', 'Livro deletado com sucesso!')
            self.carregar_livros()  # Recarrega a lista de livros após deletar
        else:
            QMessageBox.warning(self, 'Erro', 'Selecione um livro para deletar!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from firebase_admin import credentials, firestore, initialize_app

    if not firebase_admin._apps:
        cred = credentials.Certificate('firebase_config.json')
        initialize_app(cred)
    db = firestore.client()

    ex = LivroCadastroApp(db)
    ex.show()
    sys.exit(app.exec_())