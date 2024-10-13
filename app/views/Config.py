from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from app.ui.ui_config import Ui_FormConfig  # Importe a classe gerada do arquivo .ui
from helpers.auth import AuthManager
from database.connect import DatabaseManager
from helpers.message import  MessageHelper

class ConfigWindow(QWidget, Ui_FormConfig):

    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.setupUi(self)
        self.database = DatabaseManager()

        # Conecte o botão à função de salvar
        self.btn_aplicar.clicked.connect(self.save)

    def save(self):
        try:
            # Verifica se o campo edt_server está preenchido
            if not self.edt_server.text().strip():
                raise ValueError('Campo de servidor não preenchido')

            if self.edt_port.text().strip():
                # Verifica se o campo de porta é numérico
                if not self.edt_port.text().isdigit():
                    raise ValueError('A porta deve ser um número')

            # Organiza os dados a serem salvos
            data = {
                'id': 1,
                'api_url': self.edt_server.text(),
                'api_port': self.edt_port.text(),
                'refresh_interval': 30,
            }

            # Tenta inserir ou atualizar os dados no banco
            result = self.database.insert_or_update('config', data=data, where='id = 1')

            if result:  # Verifica se a operação foi bem-sucedida
                MessageHelper.show_success('Configurações salvas com sucesso')
                self.close()
            else:
                raise Exception('Erro ao salvar configurações no banco de dados')

        except ValueError as ve:
            # Captura erros de validação e exibe uma mensagem de erro
            MessageHelper.show_error(str(ve))

        except Exception as e:
            # Captura outros erros e exibe uma mensagem de erro  
            MessageHelper.show_error(f"Ocorreu um erro: {str(e)}")
