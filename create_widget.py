from PyQt5 import QtCore, QtGui, QtWidgets

class checkbox:
    def __init__(self) -> None:
        pass
    def create(self, frame,text,layout):
        check = QtWidgets.QCheckBox(frame)
        check.setObjectName("check")
        check.setText(text)
        layout.addWidget(check)
        return check