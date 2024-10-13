from PyQt5.QtWidgets import QMessageBox

class MessageHelper:

    @staticmethod
    def show_message(message, title="Mensagem", icon=QMessageBox.Information, buttons=QMessageBox.Ok):
        """
        Exibe uma mensagem parametrizada.

        :param message: Conteúdo da mensagem a ser exibida.
        :param title: Título da janela de mensagem.
        :param icon: Tipo de ícone da mensagem (QMessageBox.Information, QMessageBox.Warning, etc.).
        :param buttons: Botões disponíveis na mensagem (QMessageBox.Ok, QMessageBox.Cancel, etc.).
        """
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(buttons)
        return msg_box.exec_()

    @staticmethod
    def show_error(message, title="Erro"):
        """
        Exibe uma mensagem de erro.

        :param message: Conteúdo da mensagem de erro.
        :param title: Título da janela de erro.
        """
        return MessageHelper.show_message(message, title, QMessageBox.Warning, QMessageBox.Ok)

    @staticmethod
    def show_success(message, title="Sucesso"):
        """
        Exibe uma mensagem de sucesso.

        :param message: Conteúdo da mensagem de sucesso.
        :param title: Título da janela de sucesso.
        """
        return MessageHelper.show_message(message, title, QMessageBox.Information, QMessageBox.Ok)

    @staticmethod
    def show_warning(message, title="Aviso"):
        """
        Exibe uma mensagem de aviso.

        :param message: Conteúdo da mensagem de aviso.
        :param title: Título da janela de aviso.
        """
        return MessageHelper.show_message(message, title, QMessageBox.Warning, QMessageBox.Ok)

    @staticmethod
    def show_question(message, title="Confirmação"):
        """
        Exibe uma mensagem de confirmação com botões "Sim" e "Não".

        :param message: Conteúdo da mensagem de confirmação.
        :param title: Título da janela de confirmação.
        :return: Retorna o botão clicado (QMessageBox.Yes ou QMessageBox.No).
        """
        return MessageHelper.show_message(message, title, QMessageBox.Question, QMessageBox.Yes | QMessageBox.No)
