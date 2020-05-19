from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import *
from RESULT.gui.ui_standart_window import Ui_Dialog
from RESULT.gui.window1 import window1
from RESULT.gui.window2 import window2


class Example(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.nextButton.setEnabled(True)
        self.nextButton.clicked.connect(self.nextWindow)
        self.win1 = window1(self)

    def nextWindow(self):
        self.windows.setCurrentIndex(self.windows.currentIndex()+1)
        self.nextButton.setEnabled(False)
        if self.windows.currentIndex() == 1:
            self.win2 = window2(self, [[100, 250], [350, 400], [1234893, 8784386]])
            # self.win2 = window2(self, self.win1.main_Processing.audioProcessing.intervals_voices)


if __name__ == '__main__':
    app = QApplication([])
    form = Example()
    form.show()
    app.exec()
