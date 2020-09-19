from threading import Thread
from RESULT.OtherProcessing import *
from RESULT.gui.settings_intervals_window import settings_intervals_window


class window3:
    def __init__(self, mainGUI, main_Processing, intervals_not_presenter):
        self.intervals_not_presenter = intervals_not_presenter
        mainGUI.textBox_status_3.append("Настройте параметры!\n")
        mainGUI.startVideoAnalyze_button.setVisible(False)
        mainGUI.setParameters_button.clicked.connect(lambda: self.setParameters(mainGUI))
        mainGUI.startVideoAnalyze_button.clicked.connect(lambda: self.startVideoAnalyze(mainGUI, main_Processing))
        mainGUI.editingIntervals_pushButton.clicked.connect(lambda: self.createChildWindow(mainGUI=mainGUI,
                                                                                           main_Processing=main_Processing))

    def setParameters(self, mainGUI):
        mainGUI.setParameters_groupBox.setEnabled(False)
        mainGUI.startVideoAnalyze_button.setVisible(True)

    def startVideoAnalyze(self, mainGUI, main_Processing):
        mainGUI.startVideoAnalyze_button.setEnabled(False)
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
        self.intervals_someone = main_Processing.videoProcessing.intervals_someone
        self.intervals_someone = correct_intervals(intervals=self.intervals_someone,
                                                   maxSilence=0)
        self.intervals_together = extractOtherIntervals(intervalsA=self.intervals_not_presenter,
                                                        intervalsB=self.intervals_someone)
        for interval in self.intervals_together:
            if abs(interval[1] - interval[0]) < main_Processing.audioProcessing.minLengthFrameMs:
                self.intervals_someone.append(interval)
        self.intervals_together = [interval for interval in self.intervals_together
                                   if interval not in self.intervals_someone]
        if len(self.intervals_someone) > 0:
            insertInTextBoxIntervals(intervals=self.intervals_someone,
                                     textbox=mainGUI.textBox_intervalsSomeone)
        else:
            mainGUI.textBox_intervalsSomeone.append("No!")
        if len(self.intervals_together) > 0:
            insertInTextBoxIntervals(intervals=self.intervals_together,
                                     textbox=mainGUI.textBox_intervalsTogether)
        else:
            mainGUI.textBox_intervalsTogether.append("No!")
        mainGUI.textBox_status.append(
            "Для редактирования полученных интервалов нажмите на соответствующую кнопку!\n")
        mainGUI.textBox_status_3.append("Для завершения работы нажмите 'Завершить'!\n")
        mainGUI.nextButton.setText("Завершить")
        mainGUI.editingIntervals_pushButton.setVisible(True)
        mainGUI.nextButton.setEnabled(True)

    def createChildWindow(self, mainGUI, main_Processing):
        form = settings_intervals_window(intervals=self.intervals_together,
                                         another_intervals=self.intervals_someone,
                                         data_intervals=(
                                             main_Processing.audioProcessing.path_audio + "intervals_together/",
                                             self.intervals_together,
                                             main_Processing.audioProcessing.SR),
                                         data_another_intervals=(
                                             main_Processing.audioProcessing.path_audio + "intervals_someone/",
                                             self.intervals_someone,
                                             main_Processing.audioProcessing.SR),
                                         parent=mainGUI)
        form.label_4.setText('Интервалы ведущего и участника вместе')
        form.alternativeIntervals_groupBox.setTitle('Интервалы участника')
        form.exec_()
        self.intervals_together = form.new_intervals
        self.intervals_someone = extractOtherIntervals(intervalsA=self.intervals_not_presenter,
                                                       intervalsB=self.intervals_together)
        self.intervals_someone = correct_intervals(intervals=self.intervals_someone,
                                                   maxSilence=0)
        mainGUI.textBox_intervalsSomeone.clear()
        if len(self.intervals_someone) > 0:
            insertInTextBoxIntervals(intervals=self.intervals_someone,
                                     textbox=mainGUI.textBox_intervalsSomeone)
        else:
            mainGUI.textBox_intervalsSomeone.append("No!")
        mainGUI.textBox_intervalsTogether.clear()
        if len(self.intervals_together) > 0:
            insertInTextBoxIntervals(intervals=self.intervals_together,
                                     textbox=mainGUI.textBox_intervalsTogether)
        else:
            mainGUI.textBox_intervalsTogether.append("No!")
