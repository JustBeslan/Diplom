from threading import Thread

from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QMessageBox
from RESULT.OtherProcessing import *


class window2:
    intervals_not_presenter = []
    intervals_presenter = []

    def __init__(self, mainGUI, main_Processing):
        self.corrected_intervals_voices = correct_intervals(intervals=main_Processing.audioProcessing.intervals_voices,
                                                            maxSilence=main_Processing.audioProcessing.maxSilenceMs)
        self.corrected_intervals_voices2 = [msToTime(self.corrected_intervals_voices[i]) for i in
                                            range(len(self.corrected_intervals_voices))]
        mainGUI.trainClassificator_groupBox.setVisible(False)
        mainGUI.settingsIntervals_groupBox.setVisible(False)
        mainGUI.saveMode_button.clicked.connect(lambda: self.setTypeWork(mainGUI))
        mainGUI.deleteInterval_button.clicked.connect(lambda: self.deleteInterval(mainGUI))
        mainGUI.clearAllIntervals_button.clicked.connect(lambda: self.clearAllIntervals(mainGUI))
        mainGUI.addAllIntervals_button.clicked.connect(lambda: self.addAllIntervals(mainGUI))
        mainGUI.saveIntervals_button.clicked.connect(lambda: self.saveIntervals(mainGUI, main_Processing))
        mainGUI.trainClassificator_button.clicked.connect(lambda: self.trainClassificator(mainGUI, main_Processing))

    def setTypeWork(self, mainGUI):
        mainGUI.typeWork_groupBox.setEnabled(False)
        mainGUI.textBox_status_2.append("Режим работы установлен!\n")
        if mainGUI.manuallyWork_radioButton.isChecked():
            mainGUI.textBox_status_2.append("Откорректируйте интервалы!\n")
            mainGUI.settingsIntervals_groupBox.setVisible(True)
            mainGUI.addChange_button.setText("Добавить")
            mainGUI.intervals1_groupBox.setTitle("Ваши интервалы голоса НЕ ведущего")
            mainGUI.intervals2_groupBox.setTitle("Выделенные интервалы голосов")
            for i in range(len(self.corrected_intervals_voices)):
                hours_interval, minutes_interval, seconds_interval, milliseconds_interval = \
                    self.corrected_intervals_voices2[i]
                mainGUI.intervals2_listBox.addItem(
                    str(hours_interval[0]) + '.' + str(minutes_interval[0]) + '.' + str(
                        seconds_interval[0]) + '.' + str(milliseconds_interval[0]) + '__' + str(
                        self.corrected_intervals_voices[i][0]) + ' - ' +
                    str(hours_interval[1]) + '.' + str(minutes_interval[1]) + '.' + str(
                        seconds_interval[1]) + '.' + str(milliseconds_interval[1]) + '__' + str(
                        self.corrected_intervals_voices[i][1]))
            mainGUI.intervals2_listBox.itemClicked.connect(lambda: self.correctInterval(mainGUI=mainGUI,
                                                                                        listBox=mainGUI.intervals2_listBox))
            mainGUI.addChange_button.clicked.connect(lambda: self.addInterval(mainGUI))
        else:
            mainGUI.textBox_status_2.append("Введите небольшой интервал голоса ведущего (больше 2х секунд) "
                                            "для тренировки классификатора!\n")
            mainGUI.trainClassificator_groupBox.setVisible(True)

    def correctInterval(self, mainGUI, listBox):
        if len(listBox.selectedItems()) == 1:
            selectionInterval = str(listBox.selectedItems()[0].text())
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

            if listBox == mainGUI.intervals2_listBox:
                mainGUI.fromInterval_timeEdit.setMinimumTime(timeFromInterval)
                mainGUI.fromInterval_timeEdit.setMaximumTime(timeToInterval)
                mainGUI.toInterval_timeEdit.setMinimumTime(timeFromInterval)
                mainGUI.toInterval_timeEdit.setMaximumTime(timeToInterval)
            mainGUI.fromInterval_timeEdit.setTime(timeFromInterval)
            mainGUI.toInterval_timeEdit.setTime(timeToInterval)

    def addInterval(self, mainGUI):
        fromTimeEdit = mainGUI.fromInterval_timeEdit
        toTimeEdit = mainGUI.toInterval_timeEdit
        if fromTimeEdit.time() < toTimeEdit.time():
            strInterval = fromTimeEdit.text() + '__' + str(timeToMS(mainGUI.fromInterval_timeEdit.time())) + \
                          ' - ' + toTimeEdit.text() + '__' + str(timeToMS(mainGUI.toInterval_timeEdit.time()))
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

    def isIntersectionIntervals(self, interval1, interval2):
        interval1 = str(interval1).split(' - ')
        interval1 = [int(interval1[0].split('__')[1]), int(interval1[1].split('__')[1])]
        interval2 = str(interval2).split(' - ')
        interval2 = [int(interval2[0].split('__')[1]), int(interval2[1].split('__')[1])]
        if interval2[0] < interval1[0] < interval2[1] or interval2[0] < interval1[1] < interval2[1]:
            return True
        if interval1[0] < interval2[0] < interval1[1] or interval1[0] < interval2[1] < interval1[1]:
            return True
        return False

    def saveIntervals(self, mainGUI, main_Processing):
        isGoodIntervals = True
        for i in range(0, mainGUI.intervals1_listBox.count()):
            for j in range(i, mainGUI.intervals1_listBox.count()):
                if self.isIntersectionIntervals(interval1=mainGUI.intervals1_listBox.item(i).text(),
                                                interval2=mainGUI.intervals1_listBox.item(j).text()):
                    isGoodIntervals = False
                    QMessageBox.about(mainGUI,
                                      "Невозможно сохранить интервалы!",
                                      "Есть пересекающиеся интервалы!\n" +
                                      "Интервал 1 : " + mainGUI.intervals1_listBox.item(i).text() + "\n" +
                                      "Интервал 2 : " + mainGUI.intervals1_listBox.item(j).text() + "\n")
                    break
        if isGoodIntervals:
            mainGUI.settingsIntervals_groupBox.setEnabled(False)
            self.intervals_not_presenter = []
            for i in range(0, mainGUI.intervals1_listBox.count()):
                interval = str(mainGUI.intervals1_listBox.item(i).text()).split(' - ')
                interval = [int(interval[0].split('__')[1]), int(interval[1].split('__')[1])]
                self.intervals_not_presenter.append(interval)   # Собираем интервалы, откорректированные пользователем
            self.intervals_presenter = extractOtherIntervals(intervalsA=self.corrected_intervals_voices,
                                                             intervalsB=self.intervals_not_presenter)   # Удаляем интервалы НЕ ведущего из интервалов голосов для получения интервалов ведущего
            self.intervals_presenter = correct_intervals(intervals=self.intervals_presenter,
                                                         maxSilence=main_Processing.audioProcessing.maxSilenceMs)   # Склеиваем интервалы ведущего, забирая мелкие интервалы НЕ ведущего
            self.intervals_not_presenter = correct2_intervals(intervalsA=self.intervals_presenter,
                                                              intervalsB=self.intervals_not_presenter)  # Удаляем те интервалы НЕ ведущего, которые попали целиком под интервал голоса ведущего
            for interval in self.intervals_presenter:
                if abs(interval[1] - interval[0]) < main_Processing.audioProcessing.maxSilenceMs:
                    self.intervals_not_presenter.append(interval)   # Добавляем к интервалам НЕ ведущего те интервалы ведущего, которые по длине маленькие
            self.intervals_not_presenter = correct_intervals(intervals=self.intervals_not_presenter,
                                                             maxSilence=0)  # После добавлений выше, склеиваем соседние интервалы НЕ ведущего
            self.intervals_presenter = [interval for interval in self.intervals_presenter
                                        if interval not in self.intervals_not_presenter]    # Удаляем из интервалов ведущего те интервалы, которые попали(по длине) к интервалам НЕ ведущего
            for interval in self.intervals_presenter:
                hours_interval, minutes_interval, seconds_interval, milliseconds_interval = msToTime(interval)
                mainGUI.textBox_intervalsPresenter.append(
                    str(hours_interval[0]) + '.' + str(minutes_interval[0]) + '.' + str(
                        seconds_interval[0]) + '.' + str(milliseconds_interval[0]) + '__' + str(
                        interval[0]) + ' - ' +
                    str(hours_interval[1]) + '.' + str(minutes_interval[1]) + '.' + str(
                        seconds_interval[1]) + '.' + str(milliseconds_interval[1]) + '__' + str(
                        interval[1]) + "\n")
            mainGUI.textBox_status_2.append("Интервалы успешно сохранены!\n")
            mainGUI.textBox_status_2.append("Нажмите 'Далее'!\n")
            mainGUI.nextButton.setEnabled(True)

    def classificationIntervals(self, main_Processing, mainGUI):
        indexesIntervalsNotPresenter = main_Processing.classificator_presenter.Classification()
        self.intervals_not_presenter = [interval for i, interval in
                                        enumerate(main_Processing.audioProcessing.intervals_voices)
                                        if i in indexesIntervalsNotPresenter]
        self.corrected_intervals_not_presenter = correct_intervals(intervals=self.intervals_not_presenter,
                                                                   maxSilence=main_Processing.audioProcessing.maxSilenceMs)
        self.corrected_intervals_not_presenter = [[fromInterval, toInterval] for fromInterval, toInterval in
                                                  self.corrected_intervals_not_presenter
                                                  if abs(toInterval - fromInterval) >=
                                                  main_Processing.audioProcessing.maxSilenceMs]
        self.corrected_intervals_not_presenter2 = [msToTime(self.corrected_intervals_not_presenter[i]) for i in
                                                   range(len(self.corrected_intervals_not_presenter))]
        mainGUI.addChange_button.setText("Изменить")
        mainGUI.intervals1_groupBox.setTitle("Выделенные интервалы голоса НЕ ведущего")
        mainGUI.intervals2_groupBox.setTitle("Выделенные интервалы голосов")
        mainGUI.settingsIntervals_groupBox.setVisible(True)
        mainGUI.addAllIntervals_button.setEnabled(False)
        for i in range(len(self.corrected_intervals_voices)):
            hours_interval, minutes_interval, seconds_interval, milliseconds_interval = \
                self.corrected_intervals_voices2[i]
            mainGUI.intervals2_listBox.addItem(
                str(hours_interval[0]) + '.' + str(minutes_interval[0]) + '.' + str(
                    seconds_interval[0]) + '.' + str(milliseconds_interval[0]) + '__' + str(
                    self.corrected_intervals_voices[i][0]) + ' - ' +
                str(hours_interval[1]) + '.' + str(minutes_interval[1]) + '.' + str(
                    seconds_interval[1]) + '.' + str(milliseconds_interval[1]) + '__' + str(
                    self.corrected_intervals_voices[i][1]))
        for i in range(len(self.corrected_intervals_not_presenter)):
            hours_interval, minutes_interval, seconds_interval, milliseconds_interval = \
                self.corrected_intervals_not_presenter2[i]
            mainGUI.intervals1_listBox.addItem(
                str(hours_interval[0]) + '.' + str(minutes_interval[0]) + '.' + str(
                    seconds_interval[0]) + '.' + str(milliseconds_interval[0]) + '__' + str(
                    self.corrected_intervals_not_presenter[i][0]) + ' - ' +
                str(hours_interval[1]) + '.' + str(minutes_interval[1]) + '.' + str(
                    seconds_interval[1]) + '.' + str(milliseconds_interval[1]) + '__' + str(
                    self.corrected_intervals_not_presenter[i][1]))

    def trainClassificator(self, mainGUI, main_Processing):
        mainGUI.trainClassificator_groupBox.setEnabled(False)
        mainGUI.textBox_status_2.append("Идет тренировка классификатора...\n")
        mainGUI.repaint()
        interval = [timeToMS(mainGUI.fromIntervalPresenter_timeEdit.time()),
                    timeToMS(mainGUI.toIntervalPresenter_timeEdit.time())]
        t = Thread(target=main_Processing.GetIntervalsPresenter,
                   args=(interval,))
        t.start()
        t.join()
        mainGUI.textBox_status_2.append("Тренировка классификатора завершена!\n")
        mainGUI.textBox_status_2.append("Идет классификация интервалов...\n")
        mainGUI.repaint()
        t = Thread(target=self.classificationIntervals,
                   args=(main_Processing, mainGUI))
        t.start()
        t.join()
        mainGUI.textBox_status_2.append("Классификация интервалов завершена!\n")
        mainGUI.intervals1_listBox.itemClicked.connect(lambda: self.correctInterval(mainGUI=mainGUI,
                                                                                    listBox=mainGUI.intervals1_listBox))
        mainGUI.addChange_button.clicked.connect(lambda: self.changedInterval(mainGUI))

    def changedInterval(self, mainGUI):
        fromTimeEdit = mainGUI.fromInterval_timeEdit
        toTimeEdit = mainGUI.toInterval_timeEdit
        if fromTimeEdit.time() < toTimeEdit.time():
            strInterval = fromTimeEdit.text() + '__' + str(timeToMS(mainGUI.fromInterval_timeEdit.time())) + \
                          ' - ' + toTimeEdit.text() + '__' + str(timeToMS(mainGUI.toInterval_timeEdit.time()))
            isExists = [i1 for i1 in range(mainGUI.intervals1_listBox.count())
                        if mainGUI.intervals1_listBox.item(i1).text() == strInterval]
            if len(isExists) == 0:
                mainGUI.intervals1_listBox.selectedItems()[0].setText(strInterval)
            else:
                QMessageBox.about(mainGUI, "Невозможно добавить интервал!", "Такой интервал уже есть в списке!")
