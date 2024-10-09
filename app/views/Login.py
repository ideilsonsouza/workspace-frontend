from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from app.ui.ui_login import Ui_FormLogin  # Importe a classe gerada do arquivo .ui
from helpers.auth import AuthManager

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
        username = self.txt_user.text()
        password = self.txt_password.text()

        try:
            # Aqui você pode chamar a classe AuthManager para verificar as credenciais
            auth_manager = AuthManager()
            response = auth_manager.authenticate(username=username, password=password)
            print(response)
            if response.get('token'):
                # Se o login for bem-sucedido, emita o sinal login_success
                self.login_success.emit()
                self.close()
            else:
                # Se o login falhar, exiba uma mensagem de erro
                self.txt_password.setPlaceholderText("Credenciais inválidas")

        except Exception as e:
            # Se ocorrer algum erro, exiba uma mensagem de erro
            self.show_error_message(response.get('message'))
            self.txt_password.setPlaceholderText("Erro ao realizar login")
            self.txt_password.setPlaceholderText(str(e))
            print(e)


    def show_error_message(self,  message="Erro de login"):
        """
        Exibe uma mensagem de erro caso as credenciais estejam incorretas.
        """
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Erro")
        msg.exec_()
