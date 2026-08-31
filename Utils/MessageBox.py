from PySide6.QtWidgets import QMessageBox


class ConfirmDialog(QMessageBox):
    def __init__(self, title, text):
        """
        汎用確認ダイアログ
        :param title: ダイアログのタイトル
        :param text: ダイアログの本文
        """
        super(ConfirmDialog, self).__init__()
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QMessageBox.Icon.Question)
        self.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)


class InfoDialog(QMessageBox):
    def __init__(self, title, text):
        super(InfoDialog, self).__init__()
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QMessageBox.Icon.Information)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
