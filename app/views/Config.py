from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from app.ui.ui_config import Ui_FormConfig  # Importe a classe gerada do arquivo .ui
from helpers.auth import AuthManager

class ConfigWindow(QWidget, Ui_FormConfig):

    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.setupUi(self)