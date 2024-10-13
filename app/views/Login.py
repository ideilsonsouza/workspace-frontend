from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from app.ui.ui_login import Ui_FormLogin  # Importe a classe gerada do arquivo .ui
from helpers.auth import AuthManager
from helpers.message import MessageHelper

class LoginWindow(QWidget, Ui_FormLogin):
    # Sinal que será emitido quando o login for bem-sucedido
    login_success = pyqtSignal()

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)

        # Conectar o botão de login ao método que irá validar o login
        self.btn_login.clicked.connect(self.handle_login)

    def handle_login(self):
        """
        Método responsável por validar o login.
        Aqui você pode adicionar a lógica para verificar as credenciais.
        """
        username = self.txt_user.text().strip()
        password = self.txt_password.text().strip()

        try:
            # Verificação de campos vazios
            if not username or not password:
                raise ValueError("Username ou senha não podem ser vazios")

            # Chamar a classe AuthManager para verificar as credenciais
            auth_manager = AuthManager()
            response = auth_manager.authenticate(username=username, password=password)

            if response.get('token'):
                # Se o login for bem-sucedido, emita o sinal login_success
                self.login_success.emit()
                self.close()
            else:
                # Se o login falhar, exiba uma mensagem de erro
                MessageHelper.show_error("Credenciais inválidas")

        except ValueError as ve:
            # Se houver erro de valor (por exemplo, campos vazios), exibe a mensagem
            MessageHelper.show_error(str(ve))

        except Exception as e:
            # Se ocorrer outro erro inesperado, exibe a mensagem de erro
            MessageHelper.show_error(f"Ocorreu um erro: {str(e)}")
