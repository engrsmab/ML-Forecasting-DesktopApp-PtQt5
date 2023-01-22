from PyQt5.QtWidgets import QMessageBox
def error_dialog(heading,text,info=None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setInformativeText(info)
    msg.setWindowTitle(heading)
    msg.exec_()
def ask_dialog(heading,text,info):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText(text)
    msg.setInformativeText(info)
    msg.setWindowTitle(heading)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    data = msg.exec_()
    return data
def info_dialog(heading,text,info):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setInformativeText(info)
    msg.setWindowTitle(heading)
    msg.exec_()

