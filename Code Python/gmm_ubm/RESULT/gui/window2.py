from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QMessageBox
import numpy as np


class window2:
    msec_in_hour = 3600000
    msec_in_minute = 60000
    msec_in_sec = 1000

    def __init__(self, mainGUI, intervals_voices):
        self.intervals_voices = intervals_voices
        self.intervals_voices2 = [self.msToTime(self.intervals_voices[i]) for i in range(len(self.intervals_voices))]
        mainGUI.trainClassificator_groupBox.setVisible(False)
        mainGUI.settingsIntervals_groupBox.setVisible(False)
        mainGUI.saveMode_button.clicked.connect(lambda: self.setTypeWork(mainGUI))
        mainGUI.deleteInterval_button.clicked.connect(lambda: self.deleteInterval(mainGUI))
        mainGUI.clearAllIntervals_button.clicked.connect(lambda: self.clearAllIntervals(mainGUI))
        mainGUI.addAllIntervals_button.clicked.connect(lambda: self.addAllIntervals(mainGUI))
        mainGUI.saveIntervals_button.clicked.connect(lambda: self.saveIntervals(mainGUI))

    def msToTime(self, interval):
        interval = np.array(interval)
        hours_interval = interval // self.msec_in_hour
        minutes_interval = (interval -
                            hours_interval * self.msec_in_hour) // self.msec_in_minute
        seconds_interval = (interval -
                            hours_interval * self.msec_in_hour -
                            minutes_interval * self.msec_in_minute) // self.msec_in_sec
        milliseconds_interval = (interval -
                                 hours_interval * self.msec_in_hour -
                                 minutes_interval * self.msec_in_minute-
                                 seconds_interval * self.msec_in_sec)
        return hours_interval, minutes_interval, seconds_interval, milliseconds_interval

    def setTypeWork(self, mainGUI):
        mainGUI.typeWork_groupBox.setEnabled(False)
        mainGUI.textBox_status_2.append("Режим работы установлен!\n")
        mainGUI.textBox_status_2.append("Откорректируйте интервалы!\n")
        if mainGUI.manuallyWork_radioButton.isChecked():
            mainGUI.settingsIntervals_groupBox.setVisible(True)
            mainGUI.addChange_button.setText("Добавить")
            mainGUI.intervals1_groupBox.setTitle("Ваши интервалы голоса НЕ ведущего")
            mainGUI.intervals2_groupBox.setTitle("Выделенные интервалы голосов")
            for i in range(len(self.intervals_voices)):
                hours_interval, minutes_interval, seconds_interval, milliseconds_interval = self.intervals_voices2[i]
                mainGUI.intervals2_listBox.addItem(
                    str(hours_interval[0]) + '.' + str(minutes_interval[0]) + '.' + str(seconds_interval[0]) + '.' + str(milliseconds_interval[0]) + '__' + str(self.intervals_voices[i][0]) + ' - ' +
                    str(hours_interval[1]) + '.' + str(minutes_interval[1]) + '.' + str(seconds_interval[1]) + '.' + str(milliseconds_interval[1]) + '__' + str(self.intervals_voices[i][1]))
            mainGUI.intervals2_listBox.itemClicked.connect(lambda: self.correctInterval(mainGUI=mainGUI))
            mainGUI.addChange_button.clicked.connect(lambda: self.addInterval(mainGUI))

    def correctInterval(self, mainGUI):
        if len(mainGUI.intervals2_listBox.selectedItems()) == 1:
            selectionInterval = str(mainGUI.intervals2_listBox.selectedItems()[0].text())
            fromInterval, toInterval = selectionInterval.split(' - ')
            intervals = [fromInterval.split('__')[0], toInterval.split('__')[0]]
            hourFromInterval, minuteFromInterval, secondFromInterval, millisecondFromInterval = intervals[0].split('.')
            hourToInterval, minuteToInterval, secondToInterval, millisecondToInterval = intervals[1].split('.')
            timeFromInterval = QTime()
            timeFromInterval.setHMS(int(hourFromInterval), int(minuteFromInterval), int(secondFromInterval), int(millisecondFromInterval))
            timeToInterval = QTime()
            timeToInterval.setHMS(int(hourToInterval), int(minuteToInterval), int(secondToInterval), int(millisecondToInterval))

            mainGUI.fromInterval_timeEdit.setMinimumTime(timeFromInterval)
            mainGUI.fromInterval_timeEdit.setMaximumTime(timeToInterval)
            mainGUI.fromInterval_timeEdit.setTime(timeFromInterval)

            mainGUI.toInterval_timeEdit.setMinimumTime(timeFromInterval)
            mainGUI.toInterval_timeEdit.setMaximumTime(timeToInterval)
            mainGUI.toInterval_timeEdit.setTime(timeToInterval)


    def timeToMS(self, time):
        return time.hour() * self.msec_in_hour + time.minute() * self.msec_in_minute + time.second() * self.msec_in_sec + time.msec()

    def addInterval(self, mainGUI):
        fromTimeEdit = mainGUI.fromInterval_timeEdit
        toTimeEdit = mainGUI.toInterval_timeEdit
        if fromTimeEdit.time() < toTimeEdit.time():
            strInterval = fromTimeEdit.text() + '__' + str(self.timeToMS(mainGUI.fromInterval_timeEdit.time())) + \
                          ' - ' + toTimeEdit.text() + '__' + str(self.timeToMS(mainGUI.toInterval_timeEdit.time()))
            isExists = [i1 for i1 in range(mainGUI.intervals1_listBox.count())
                        if mainGUI.intervals1_listBox.item(i1).text() == strInterval]
            if len(isExists) == 0:
                mainGUI.intervals1_listBox.addItem(strInterval)
            else:
                QMessageBox.about(mainGUI, "Невозможно добавить интервал!", "Такой интервал уже есть в списке!")
        else:
            QMessageBox.about(mainGUI, "Невозможно добавить интервал!", "Интервал не является корректным!!!")

    def deleteInterval(self, mainGUI):
        mainGUI.intervals1_listBox.takeItem(mainGUI.intervals1_listBox.currentRow())

    def clearAllIntervals(self, mainGUI):
        mainGUI.intervals1_listBox.clear()

    def addAllIntervals(self, mainGUI):
        if len(mainGUI.intervals2_listBox.selectedItems()) > 1:
            for item in mainGUI.intervals2_listBox.selectedItems():
                isExists = [i1 for i1 in range(mainGUI.intervals1_listBox.count())
                            if mainGUI.intervals1_listBox.item(i1).text() == item.text()]
                if len(isExists) == 0:
                    mainGUI.intervals1_listBox.addItem(item.text())
        else:
            for i in range(mainGUI.intervals2_listBox.count()):
                isExists = [i1 for i1 in range(mainGUI.intervals1_listBox.count())
                            if mainGUI.intervals1_listBox.item(i1).text() == mainGUI.intervals2_listBox.item(i).text()]
                if len(isExists) == 0:
                    mainGUI.intervals1_listBox.addItem(mainGUI.intervals2_listBox.item(i).text())

    def saveIntervals(self, mainGUI):
        mainGUI.settingsIntervals_groupBox.setEnabled(False)
        mainGUI.textBox_status_2.append("Интервалы успешно сохранены!\n")
        
