import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from database.connect import DatabaseManager
from helpers.auth import AuthManager
from app.views.Config import ConfigWindow  # Tela de configurações (deve ser criada)
from app.views.Login import LoginWindow    # Tela de login (deve ser criada)
from app.ui.ui_main import Ui_MainForm      # Tela principal (deve ser criada)


class AppController:
    def __init__(self):
        self.db = DatabaseManager()
        self.auth_manager = AuthManager()
        self.config_window = None
        self.login_window = None
        self.main_window = None
        self.attempts = 0  # Contador de tentativas de autenticação falhas

    def check_configurations(self):
        """
        Verifica se as configurações estão presentes. Se não, abre a tela de configurações.
        """
        config = self.db.get_single_record('config', where="id = 1")
        if isinstance(config, str) and config == "[]":
            self.show_config_window()  # Exibe a tela de configurações
        else:
            self.check_token()

    def check_token(self):
        """
        Verifica se há um token armazenado. Se houver, tenta autenticar.
        """
        token = self.db.get_single_record('token', where="id = 1")
        if isinstance(token, str) and token != "[]":
            # Testar o token com a API
            response = self.auth_manager.make_request("GET", "/check_token")
            if response is None and self.attempts < 2:
                self.attempts += 1
                self.show_login_window()  # Se falhar, mostra a tela de login
            else:
                self.show_main_window()  # Se for bem-sucedido, exibe a tela principal
        else:
            self.show_login_window()  # Se não houver token, exibe a tela de login

    def show_config_window(self):
        """
        Exibe a tela de configurações.
        """
        self.config_window = ConfigWindow()
        self.config_window.show()
        # self.config_window.config_saved.connect(self.check_token)  # Após salvar config, verificar o token

    def show_login_window(self):
        """
        Exibe a tela de login.
        """
        self.login_window = LoginWindow()
        self.login_window.login_success.connect(self.check_token)  # Após login, verificar o token
        self.login_window.show()

    def show_main_window(self):
        """
        Exibe a tela principal da aplicação.
        """
        self.main_window = Ui_MainForm()
        self.main_window.show()


def main():
    app = QApplication(sys.argv)

    controller = AppController()
    controller.check_configurations()  # Inicia verificando as configurações

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
