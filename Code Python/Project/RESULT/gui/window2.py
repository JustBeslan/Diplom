from threading import Thread

from PyQt5.QtCore import QTime
from RESULT.OtherProcessing import *
from RESULT.gui.settings_intervals_window import settings_intervals_window


class window2:
    intervals_not_presenter = []
    intervals_presenter = []
    min_time = QTime()
    max_time = QTime()

    def __init__(self, mainGUI, main_Processing):
        self.corrected_intervals_voices = correct_intervals(intervals=main_Processing.audioProcessing.intervals_voices,
                                                            maxSilence=0)
        self.corrected_intervals_voices2 = [msToTime(self.corrected_intervals_voices[i]) for i in
                                            range(len(self.corrected_intervals_voices))]
        self.corrected_data_intervals_voices = []
        self.corrected_data_intervals_not_presenter = []
        for interval in self.corrected_intervals_voices:
            self.corrected_data_intervals_voices.append([])
            for j in range(interval[0] // main_Processing.audioProcessing.slice_ms,
                           interval[1] // main_Processing.audioProcessing.slice_ms):
                self.corrected_data_intervals_voices[len(self.corrected_data_intervals_voices) - 1] = \
                    self.corrected_data_intervals_voices[len(self.corrected_data_intervals_voices) - 1] + [
                        list(main_Processing.audioProcessing.partsAudio[j].flatten())]
        mainGUI.trainClassificator_groupBox.setVisible(False)
        mainGUI.saveMode_button.clicked.connect(lambda: self.createChildWindow(mainGUI=mainGUI,
                                                                               main_Processing=main_Processing))
        mainGUI.trainClassificator_button.clicked.connect(lambda: self.trainClassificator(mainGUI, main_Processing))
        mainGUI.editingIntervals_pushButton.clicked.connect(lambda: self.correctIntervals(mainGUI=mainGUI,
                                                                                          main_Processing=main_Processing))
        self.max_time.setHMS(23, 59, 59, 999)
        self.min_time.setHMS(0, 0, 0, 0)

    def createChildWindow(self, mainGUI, main_Processing):
        mainGUI.typeWork_groupBox.setEnabled(False)
        mainGUI.textBox_status_2.append("Режим работы установлен!\n")
        if mainGUI.manuallyWork_radioButton.isChecked():
            mainGUI.textBox_status_2.append("Откорректируйте интервалы!\n")
            self.correctIntervals(mainGUI, main_Processing)
        else:
            mainGUI.textBox_status_2.append("Введите небольшой интервал голоса ведущего (больше 2х секунд) "
                                            "для тренировки классификатора!\n")
            mainGUI.trainClassificator_groupBox.setVisible(True)

    def correctIntervals(self, mainGUI, main_Processing):
        if mainGUI.windows.currentIndex() == 1:
            print(len(extractOtherIntervals(intervalsA=self.corrected_intervals_voices,
                                            intervalsB=self.intervals_not_presenter)))  # Удаляем интервалы НЕ ведущего из интервалов голосов для получения интервалов ведущего
            form = settings_intervals_window(intervals=self.intervals_not_presenter,
                                             another_intervals=self.corrected_intervals_voices,
                                             data_intervals=(
                                                 main_Processing.audioProcessing.path_audio + "intervals_not_presenter/",
                                                 self.corrected_data_intervals_not_presenter,
                                                 main_Processing.audioProcessing.SR),
                                             data_another_intervals=(
                                                 main_Processing.audioProcessing.path_audio + "intervals_voices/",
                                                 self.corrected_data_intervals_voices,
                                                 main_Processing.audioProcessing.SR),
                                             parent=mainGUI)
            form.label_4.setText('Интервалы НЕ ведущего')
            form.alternativeIntervals_groupBox.setTitle('Интервалы голоса')
            form.exec_()
            self.intervals_not_presenter = form.new_intervals
            self.intervals_not_presenter = correct_intervals(intervals=self.intervals_not_presenter,
                                                             maxSilence=0)  # После добавлений выше, склеиваем соседние интервалы НЕ ведущего
            self.intervals_presenter = extractOtherIntervals(intervalsA=self.corrected_intervals_voices,
                                                             intervalsB=self.intervals_not_presenter)  # Удаляем интервалы НЕ ведущего из интервалов голосов для получения интервалов ведущего
            self.intervals_presenter = correct_intervals(intervals=self.intervals_presenter,
                                                         maxSilence=0)  # Склеиваем интервалы ведущего, забирая мелкие интервалы НЕ ведущего
            # self.intervals_not_presenter = correct2_intervals(intervalsA=self.intervals_presenter,
            #                                                   intervalsB=self.intervals_not_presenter)  # Удаляем те интервалы НЕ ведущего, которые попали целиком под интервал голоса ведущего
            for interval in self.intervals_not_presenter:
                if abs(interval[1] - interval[0]) < main_Processing.audioProcessing.minLengthFrameMs:
                    self.intervals_presenter.append(
                        interval)  # Добавляем к интервалам НЕ ведущего те интервалы ведущего, которые по длине маленькие
            self.intervals_not_presenter = [interval for interval in self.intervals_not_presenter
                                            if
                                            interval not in self.intervals_presenter]  # Удаляем из интервалов ведущего те интервалы, которые попали(по длине) к интервалам НЕ ведущего
            print(len(self.intervals_presenter))
            mainGUI.textBox_intervalsPresenter.clear()
            insertInTextBoxIntervals(intervals=self.intervals_presenter,
                                     textbox=mainGUI.textBox_intervalsPresenter)
            mainGUI.textBox_status.append(
                "Для редактирования полученных интервалов нажмите на соответствующую кнопку!\n")
            mainGUI.editingIntervals_pushButton.setVisible(True)
            mainGUI.nextButton.setEnabled(True)

    def classificationIntervals(self, main_Processing):
        indexesIntervalsNotPresenter = main_Processing.classificator_presenter.Classification()
        self.intervals_not_presenter = [interval for i, interval in
                                        enumerate(main_Processing.audioProcessing.intervals_voices)
                                        if i in indexesIntervalsNotPresenter]
        self.intervals_not_presenter = correct_intervals(intervals=self.intervals_not_presenter,
                                                         maxSilence=main_Processing.audioProcessing.maxSilenceMs)
        self.intervals_not_presenter = [[fromInterval, toInterval] for fromInterval, toInterval in
                                        self.intervals_not_presenter
                                        if abs(toInterval - fromInterval) >=
                                        main_Processing.audioProcessing.minLengthFrameMs]
        for interval in self.intervals_not_presenter:
            self.corrected_data_intervals_not_presenter.append([])
            for j in range(interval[0] // main_Processing.audioProcessing.slice_ms,
                           interval[1] // main_Processing.audioProcessing.slice_ms):
                self.corrected_data_intervals_not_presenter[len(self.corrected_data_intervals_not_presenter) - 1] += [
                    list(main_Processing.audioProcessing.partsAudio[j].flatten())]

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
                   args=(main_Processing,))
        t.start()
        t.join()
        mainGUI.textBox_status_2.append("Классификация интервалов завершена!\n")
        self.correctIntervals(mainGUI=mainGUI,
                              main_Processing=main_Processing)
