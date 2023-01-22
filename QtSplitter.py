from PyQt5 import QtGui,QtCore,QtWidgets

class QtSplitter:
    def __init__(self) -> None:
        #   self.hbox = QtWidgets.QHBoxLayout(self)
          self.vertical_split = False
          self.horizontal_split = False
    def Splitter(self,frame_1,frame_2,frames_size:list):
        if self.vertical_split:
            split = QtCore.Qt.Vertical
        elif self.horizontal_split:
            split = QtCore.Qt.Horizontal
        else:
            RuntimeWarning("Please select split oriantation")
        
        splitter = QtWidgets.QSplitter(split)
        splitter.addWidget(frame_1)
        splitter.addWidget(frame_2)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes(frames_size)
        verticalLayout_2 = QtWidgets.QVBoxLayout(splitter)
        verticalLayout_2.setSpacing(0)
        verticalLayout_2.setObjectName("verticalLayout_2")
        # self.hbox.addWidget(splitter)
        # self.setLayout(self.hbox)