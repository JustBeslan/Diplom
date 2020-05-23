import os
import shutil

import librosa
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QDialog, QMessageBox, QScrollBar, QTimeEdit
from RESULT.gui.ui_settings_intervals_window import Ui_Dialog
from RESULT.OtherProcessing import *


class settings_intervals_window(QDialog, Ui_Dialog):
    corrected_intervals = []
    corrected_another_intervals = []

    def __init__(self, intervals, another_intervals, data_intervals, data_another_intervals, parent=None):
        super(settings_intervals_window, self).__init__(parent)
        self.setupUi(self)
        for interval in intervals:
            hours_interval, minutes_interval, seconds_interval, milliseconds_interval = msToTime(interval)
            str_interval = str(hours_interval[0]) + '.' + str(minutes_interval[0]) + '.' + str(
                seconds_interval[0]) + '.' + str(milliseconds_interval[0]) + '__' + str(
                interval[0]) + ' - ' + str(hours_interval[1]) + '.' + str(minutes_interval[1]) + '.' + str(
                seconds_interval[1]) + '.' + str(milliseconds_interval[1]) + '__' + str(
                interval[1])
            self.intervals_listBox.addItem(str_interval)
            self.corrected_intervals.append(str_interval)
        self.intervals_listBox.itemClicked.connect(lambda: self.getInterval())
        self.addInterval_button.clicked.connect(lambda: self.addInterval(fromTimeEdit=self.fromInterval_timeEdit,
                                                                         toTimeEdit=self.toInterval_timeEdit))
        self.changeInterval_button.clicked.connect(lambda: self.changeInterval())
        self.deleteInterval_button.clicked.connect(lambda: self.deleteInterval())
        self.clearAllIntervals_button.clicked.connect(lambda: self.clearAllIntervals())
        self.saveIntervals_button.clicked.connect(lambda: self.saveIntervals())
        self.joinIntervals_pushButton.clicked.connect(lambda: self.joinIntervals(
            interval1=self.interval1_comboBox.currentText(),
            interval2=self.interval2_comboBox.currentText()))
        for interval in another_intervals:
            hours_interval, minutes_interval, seconds_interval, milliseconds_interval = msToTime(interval)
            str_interval = str(hours_interval[0]) + '.' + str(minutes_interval[0]) + '.' + str(
                seconds_interval[0]) + '.' + str(milliseconds_interval[0]) + '__' + str(
                interval[0]) + ' - ' + str(hours_interval[1]) + '.' + str(minutes_interval[1]) + '.' + str(
                seconds_interval[1]) + '.' + str(milliseconds_interval[1]) + '__' + str(
                interval[1])
            self.alternativeIntervals_comboBox.addItem(str_interval)
            self.corrected_another_intervals.append(str_interval)
        self.writePartsAudio(data=data_intervals,
                             intervals=self.corrected_intervals)
        self.path_dir_intervals = data_intervals[0]
        self.writePartsAudio(data=data_another_intervals,
                             intervals=self.corrected_another_intervals)
        self.path_dir_another_intervals = data_another_intervals[0]
        QMessageBox.about(self, "Записано!",
                          "Данные части аудио можно прослушать в соответствующей папке в папке 'Audio' !")
        self.addAllIntervals_pushButton.clicked.connect(lambda: self.addAllIntervals())
        self.addInterval_pushButton.clicked.connect(lambda: self.addAnotherInterval())
        self.updateComboBoxes()

    def writePartsAudio(self, data, intervals):
        if not os.path.exists(data[0]):
            os.makedirs(data[0])
        for i in range(len(data[1])):
            librosa.output.write_wav(path=data[0] + intervals[i] + '.wav',
                                     y=np.array(data[1][i]).flatten(),
                                     sr=data[2])

    def addAnotherInterval(self):
        timeFromInterval, timeToInterval = self.insertIntervalInTimeEdits(
            self.alternativeIntervals_comboBox.currentText())
        self.fromInterval_timeEdit.setTime(timeFromInterval)
        self.toInterval_timeEdit.setTime(timeToInterval)
        self.updateComboBoxes()

    def addAllIntervals(self):
        fromTimeEdit = QTimeEdit()
        toTimeEdit = QTimeEdit()
        fromTimeEdit.setDisplayFormat("H.m.s.zzz")
        toTimeEdit.setDisplayFormat("H.m.s.zzz")
        for i in range(self.alternativeIntervals_comboBox.count()):
            timeFromInterval, timeToInterval = self.insertIntervalInTimeEdits(
                self.alternativeIntervals_comboBox.itemText(i))
            fromTimeEdit.setTime(timeFromInterval)
            toTimeEdit.setTime(timeToInterval)
            self.addInterval(fromTimeEdit=fromTimeEdit,
                             toTimeEdit=toTimeEdit,
                             warnings=False)
        self.updateComboBoxes()

    def joinIntervals(self, interval1, interval2):
        interval = interval1.split(' - ')[1] + ' - ' + interval2.split(' - ')[0]
        innerIntervals = [self.intervals_listBox.item(i).text() for i in range(self.intervals_listBox.count())
                          if isIntersectionIntervals(interval, self.intervals_listBox.item(i).text())]
        if len(innerIntervals) == 0:
            timeFromInterval, timeToInterval = self.insertIntervalInTimeEdits(interval=interval)
            self.fromInterval_timeEdit.setTime(timeFromInterval)
            self.toInterval_timeEdit.setTime(timeToInterval)
        else:
            beginInterval, endInterval = interval.split(' - ')
            fromTimeEdit = QTimeEdit()
            toTimeEdit = QTimeEdit()
            fromTimeEdit.setDisplayFormat("H.m.s.zzz")
            toTimeEdit.setDisplayFormat("H.m.s.zzz")
            for i in range(len(innerIntervals) + 1):
                if i == 0:
                    innerInterval = innerIntervals[i].split(' - ')
                    current_interval = beginInterval + ' - ' + innerInterval[0]
                    beginInterval = innerInterval[1]
                elif i == len(innerIntervals):
                    innerInterval = innerIntervals[i - 1].split(' - ')
                    current_interval = innerInterval[1] + ' - ' + endInterval
                else:
                    innerInterval = innerIntervals[i].split(' - ')
                    current_interval = beginInterval + ' - ' + innerInterval[0]
                    beginInterval = innerInterval[1]
                timeFromInterval, timeToInterval = self.insertIntervalInTimeEdits(current_interval)
                fromTimeEdit.setTime(timeFromInterval)
                toTimeEdit.setTime(timeToInterval)
                self.addInterval(fromTimeEdit=fromTimeEdit,
                                 toTimeEdit=toTimeEdit,
                                 warnings=False)
        self.updateComboBoxes()

    def insertIntervalInTimeEdits(self, interval):
        interval = interval.split(' - ')
        interval = [interval_.split('__')[0] for interval_ in interval]
        hourFromInterval, minuteFromInterval, secondFromInterval, millisecondFromInterval = interval[0].split('.')
        hourToInterval, minuteToInterval, secondToInterval, millisecondToInterval = interval[1].split('.')
        timeFromInterval = QTime()
        timeFromInterval.setHMS(int(hourFromInterval), int(minuteFromInterval), int(secondFromInterval),
                                int(millisecondFromInterval))
        timeToInterval = QTime()
        timeToInterval.setHMS(int(hourToInterval), int(minuteToInterval), int(secondToInterval),
                              int(millisecondToInterval))
        return timeFromInterval, timeToInterval

    def updateComboBoxes(self):
        self.interval1_comboBox.clear()
        self.interval1_comboBox.addItems([self.intervals_listBox.item(i).text()
                                          for i in range(self.intervals_listBox.count())])
        self.interval2_comboBox.clear()
        self.interval2_comboBox.addItems([self.intervals_listBox.item(i).text()
                                          for i in range(self.intervals_listBox.count())])

    def deleteInterval(self):
        self.intervals_listBox.takeItem(self.intervals_listBox.currentRow())
        self.updateComboBoxes()

    def saveIntervals(self):
        isGoodIntervals = True
        for i in range(0, self.intervals_listBox.count()):
            for j in range(i, self.intervals_listBox.count()):
                if isIntersectionIntervals(interval1=self.intervals_listBox.item(i).text(),
                                           interval2=self.intervals_listBox.item(j).text()):
                    isGoodIntervals = False
                    QMessageBox.about(self,
                                      "Невозможно сохранить интервалы!",
                                      "Есть пересекающиеся интервалы!\n" +
                                      "Интервал 1 : " + self.intervals_listBox.item(i).text() + "\n" +
                                      "Интервал 2 : " + self.intervals_listBox.item(j).text() + "\n")
                    break
        if isGoodIntervals:
            shutil.rmtree(self.path_dir_intervals[0:-1])
            shutil.rmtree(self.path_dir_another_intervals[0:-1])
            self.new_intervals = []
            for i in range(self.intervals_listBox.count()):
                text = self.intervals_listBox.item(i).text()
                interval = text.split(' - ')
                interval = [int(interval[0].split('__')[1]),
                            int(interval[1].split('__')[1])]
                self.new_intervals.append(interval)
            self.new_intervals.sort()
            QMessageBox.about(self, "Сохранение!", "Интервалы успешно сохранены!")
            self.close()

    def clearAllIntervals(self):
        selectedItems = self.intervals_listBox.selectedItems()
        if len(selectedItems) > 1:
            for interval in selectedItems:
                self.intervals_listBox.takeItem(
                    self.intervals_listBox.row(interval))
        else:
            self.intervals_listBox.clear()
        self.updateComboBoxes()

    def getInterval(self):
        selectionInterval = str(self.intervals_listBox.selectedItems()[0].text())
        fromInterval, toInterval = selectionInterval.split(' - ')
        intervals = [fromInterval.split('__')[0], toInterval.split('__')[0]]
        hourFromInterval, minuteFromInterval, secondFromInterval, millisecondFromInterval = intervals[0].split('.')
        hourToInterval, minuteToInterval, secondToInterval, millisecondToInterval = intervals[1].split('.')
        timeFromInterval = QTime()
        timeFromInterval.setHMS(int(hourFromInterval), int(minuteFromInterval), int(secondFromInterval),
                                int(millisecondFromInterval))
        timeToInterval = QTime()
        timeToInterval.setHMS(int(hourToInterval), int(minuteToInterval), int(secondToInterval),
                              int(millisecondToInterval))
        self.fromInterval_timeEdit.setTime(timeFromInterval)
        self.toInterval_timeEdit.setTime(timeToInterval)

    def addInterval(self, fromTimeEdit, toTimeEdit, warnings=True):
        if fromTimeEdit.time() < toTimeEdit.time():
            strInterval = fromTimeEdit.text() + '__' + str(timeToMS(fromTimeEdit.time())) + \
                          ' - ' + toTimeEdit.text() + '__' + str(timeToMS(toTimeEdit.time()))
            isExists = [i1 for i1 in range(self.intervals_listBox.count())
                        if self.intervals_listBox.item(i1).text() == strInterval]
            if len(isExists) == 0:
                self.intervals_listBox.addItem(strInterval)
            elif warnings:
                QMessageBox.about(self, "Невозможно добавить интервал!", "Такой интервал уже есть в списке!")
        elif warnings:
            QMessageBox.about(self, "Невозможно добавить интервал!", "Интервал не является корректным!!!")
        self.updateComboBoxes()

    def changeInterval(self):
        fromTimeEdit = self.fromInterval_timeEdit
        toTimeEdit = self.toInterval_timeEdit
        if fromTimeEdit.time() < toTimeEdit.time():
            strInterval = fromTimeEdit.text() + '__' + str(timeToMS(self.fromInterval_timeEdit.time())) + \
                          ' - ' + toTimeEdit.text() + '__' + str(timeToMS(self.toInterval_timeEdit.time()))
            isExists = [i1 for i1 in range(self.intervals_listBox.count())
                        if self.intervals_listBox.item(i1).text() == strInterval]
            if len(isExists) == 0:
                self.intervals_listBox.selectedItems()[0].setText(strInterval)
            else:
                QMessageBox.about(self, "Невозможно добавить интервал!", "Такой интервал уже есть в списке!")
        self.updateComboBoxes()
