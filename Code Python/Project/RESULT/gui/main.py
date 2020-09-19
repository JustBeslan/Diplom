import os
import sys
from PyQt5.QtWidgets import *

from RESULT.gui.ui_standart_window import Ui_Dialog
from RESULT.gui.window1 import window1
from RESULT.gui.window2 import window2
from RESULT.gui.window3 import window3


class Example(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.nextButton.clicked.connect(self.nextWindow)
        self.win1 = window1(self)

        # pixmap = QPixmap('C:/Users/Ibrag/OneDrive/Изображения/Saved Pictures/1.jpg')
        # pixmap = pixmap.scaledToWidth(520)
        # scene = QGraphicsScene()
        # self.regionCoference_graphicsView.setScene(scene)
        # scene.addPixmap(pixmap)

    def nextWindow(self):
        self.windows.setCurrentIndex(self.windows.currentIndex() + 1)
        self.nextButton.setEnabled(False)
        self.editingIntervals_pushButton.setVisible(False)
        if self.nextButton.text() == "Далее" and self.windows.currentIndex() == 1:
            self.win2 = window2(self, self.win1.main_Processing)
        if self.nextButton.text() == "Далее" and self.windows.currentIndex() == 2:
            self.win3 = window3(self, self.win1.main_Processing, self.win2.intervals_not_presenter)
        if self.nextButton.text() == "Завершить":
            if self.saveAllIntervalsInFiles_checkBox.isChecked():
                pathResult = self.win1.main_Processing.audioProcessing.pathVideo + "Result/"
                if not os.path.exists(pathResult):
                    os.makedirs(name=pathResult)
                else:
                    for file in os.listdir(pathResult):
                        os.remove(pathResult + file)
                textIntervals = self.textBox_intervalsSilence.toPlainText()
                if textIntervals != 'No!':
                    self.saveIntervalsInFile(path_name=pathResult + "intervalsSilence.txt",
                                             intervals=textIntervals)
                textIntervals = self.textBox_intervalsPresenter.toPlainText()
                if textIntervals != 'No!':
                    self.saveIntervalsInFile(path_name=pathResult + "intervalsPresenter.txt",
                                             intervals=textIntervals)
                textIntervals = self.textBox_intervalsSomeone.toPlainText()
                if textIntervals != 'No!':
                    self.saveIntervalsInFile(path_name=pathResult + "intervalsSomeone.txt",
                                             intervals=textIntervals)
                textIntervals = self.textBox_intervalsTogether.toPlainText()
                if textIntervals != 'No!':
                    self.saveIntervalsInFile(path_name=pathResult + "intervalsTogether.txt",
                                             intervals=textIntervals)
                QMessageBox.about(self, "Успешно!", "Интервалы успешно сохранены в файлы!\n")
            sys.exit()

    def saveIntervalsInFile(self, path_name, intervals):
        f = open(path_name, 'w')
        for interval in intervals.split('\n'):
            if len(interval) > 0:
                f.write(interval + '\n')


if __name__ == '__main__':
    app = QApplication([])
    form = Example()
    form.show()
    app.exec()
