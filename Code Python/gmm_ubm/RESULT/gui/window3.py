from threading import Thread
from RESULT.OtherProcessing import *


class window3:
    def __init__(self, mainGUI, main_Processing, intervals_not_presenter):
        self.intervals_not_presenter = intervals_not_presenter
        mainGUI.textBox_status_3.append("Настройте параметры!\n")
        mainGUI.startVideoAnalyze_button.setVisible(False)
        mainGUI.setParameters_button.clicked.connect(lambda: self.setParameters(mainGUI))
        mainGUI.startVideoAnalyze_button.clicked.connect(lambda: self.startVideoAnalyze(mainGUI, main_Processing))

    def setParameters(self, mainGUI):
        mainGUI.setParameters_groupBox.setEnabled(False)
        mainGUI.startVideoAnalyze_button.setVisible(True)

    def startVideoAnalyze(self, mainGUI, main_Processing):
        mainGUI.textBox_status_3.append("Идет обработка слайдов вебинара...\n")
        mainGUI.repaint()
        t = Thread(target=main_Processing.videoAnalyse,
                   args=(self.intervals_not_presenter,
                         mainGUI.minDistance_spinBox.value(),
                         mainGUI.maxDistance_spinBox.value(),
                         mainGUI.timeBetweenFrames_spinBox.value(),
                         mainGUI.showRegionConference_checkBox.isChecked()))
        t.start()
        t.join()
        mainGUI.textBox_status_3.append("Обработка слайдов вебинара завершена!\n")
        mainGUI.textBox_status_3.append("Все типы интервалов были выделены!\n")
        mainGUI.textBox_status_3.append("Нажмите 'Завершить'!\n")
        self.intervals_someone = main_Processing.videoProcessing.intervals_someone
        self.intervals_someone = correct_intervals(intervals=self.intervals_someone,
                                                   maxSilence=main_Processing.audioProcessing.maxSilenceMs)
        self.intervals_someone = [interval for interval in self.intervals_someone
                                  if abs(interval[1] - interval[0]) >= main_Processing.audioProcessing.maxSilenceMs]
        self.intervals_together = extractOtherIntervals(intervalsA=self.intervals_not_presenter,
                                                        intervalsB=self.intervals_someone)
        if len(self.intervals_someone) > 0:
            for interval in self.intervals_someone:
                hours_interval, minutes_interval, seconds_interval, milliseconds_interval = msToTime(interval)
                mainGUI.textBox_intervalsSomeone.append(
                    str(hours_interval[0]) + '.' + str(minutes_interval[0]) + '.' + str(
                        seconds_interval[0]) + '.' + str(milliseconds_interval[0]) + '__' + str(
                        interval[0]) + ' - ' +
                    str(hours_interval[1]) + '.' + str(minutes_interval[1]) + '.' + str(
                        seconds_interval[1]) + '.' + str(milliseconds_interval[1]) + '__' + str(
                        interval[1]) + "\n")
        else:
            mainGUI.textBox_intervalsSomeone.append("No!")
        self.intervals_together = extractOtherIntervals(intervalsA=self.intervals_not_presenter,
                                                        intervalsB=self.intervals_someone)
        if len(self.intervals_together) > 0:
            for interval in self.intervals_together:
                hours_interval, minutes_interval, seconds_interval, milliseconds_interval = msToTime(interval)
                mainGUI.textBox_intervalsTogether.append(
                    str(hours_interval[0]) + '.' + str(minutes_interval[0]) + '.' + str(
                        seconds_interval[0]) + '.' + str(milliseconds_interval[0]) + '__' + str(
                        interval[0]) + ' - ' +
                    str(hours_interval[1]) + '.' + str(minutes_interval[1]) + '.' + str(
                        seconds_interval[1]) + '.' + str(milliseconds_interval[1]) + '__' + str(
                        interval[1]) + "\n")
        else:
            mainGUI.textBox_intervalsTogether.append("No!")
        mainGUI.nextButton.setText("Завершить")
        mainGUI.nextButton.setEnabled(True)
