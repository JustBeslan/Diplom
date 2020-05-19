from PyQt5.QtWidgets import QFileDialog
from RESULT.MainProcessing import Main_Processing
from threading import Thread
from RESULT.OtherProcessing import correct_intervals, correct2_intervals


class window1:
    def __init__(self, mainGUI):
        mainGUI.settingsParameters_groupBox.setVisible(False)
        mainGUI.filterButton.setVisible(False)
        mainGUI.extractSilenceButton.setVisible(False)
        mainGUI.loadVideo_pathButton.clicked.connect(lambda: self.getPathVideo(mainGUI))
        mainGUI.loadVideo_loadButton.clicked.connect(lambda: self.loadVideo(mainGUI))
        mainGUI.settingsParameters_setButton.clicked.connect(lambda: self.setParameters(mainGUI))
        mainGUI.filterButton.clicked.connect(lambda: self.filteringAudio(mainGUI))
        mainGUI.extractSilenceButton.clicked.connect(lambda: self.extractSilence(mainGUI))

    def extractSilence(self, mainGUI):
        mainGUI.extractSilenceButton.setEnabled(False)
        mainGUI.textBox_status.append("Идет извлечение тишины...\n")
        mainGUI.repaint()
        t = Thread(target=self.main_Processing.audioProcessing.ExtractVoices,
                   args=(self.main_Processing.audioProcessing.filtered_data_audio,
                         self.main_Processing.audioProcessing.SR))
        t.start()
        t.join()
        mainGUI.textBox_status.append("Извлечение тишины из аудио завершено!\n")
        mainGUI.textBox_status.append("Нажмите 'Далее'!\n")
        self.main_Processing.audioProcessing.intervals_silence = \
            correct_intervals(intervals=self.main_Processing.audioProcessing.intervals_silence,
                              maxSilence=self.main_Processing.audioProcessing.maxSilenceMs)
        self.main_Processing.audioProcessing.intervals_voices = \
            correct2_intervals(intervalsA=self.main_Processing.audioProcessing.intervals_silence,
                               intervalsB=self.main_Processing.audioProcessing.intervals_voices)
        for interval in self.main_Processing.audioProcessing.intervals_silence:
            mainGUI.textBox_intervalsSilence.append(str(interval[0]) + ' - ' + str(interval[1]))
        mainGUI.nextButton.setEnabled(True)
        print(self.main_Processing.audioProcessing.intervals_silence)
        print(self.main_Processing.audioProcessing.intervals_voices)

    def filteringAudio(self, mainGUI):
        mainGUI.filterButton.setEnabled(False)
        mainGUI.textBox_status.append("Идет фильтрация аудио...\n")
        mainGUI.repaint()
        t = Thread(target=self.main_Processing.audioProcessing.filtering_audio)
        t.start()
        t.join()
        mainGUI.textBox_status.append("Фильтрация аудио завершена!\n")
        mainGUI.extractSilenceButton.setVisible(True)

    def setParameters(self, mainGUI):
        self.main_Processing.audioProcessing.set_sliceMs(ms=mainGUI.settingsParameters_splitMs.value())
        self.main_Processing.audioProcessing.set_maxSilenceMs(ms=mainGUI.settingsParameters_maxSilenceMs.value())
        mainGUI.settingsParameters_groupBox.setEnabled(False)
        mainGUI.textBox_status.append("Параметры установлены!\n")
        mainGUI.filterButton.setVisible(True)

    def getPathVideo(self, mainGUI):
        fileName = QFileDialog.getOpenFileName()[0]
        mainGUI.loadVideo_pathEdit.setText(fileName)
        if len(mainGUI.loadVideo_pathEdit.text()) > 0:
            mainGUI.loadVideo_loadButton.setEnabled(True)

    def createMainProcessing(self, pathVideo, nameVideo):
        self.main_Processing = Main_Processing(pathVideo=pathVideo,
                                               nameVideo=nameVideo)

    def loadVideo(self, mainGUI):
        mainGUI.loadVideo_groupBox.setEnabled(False)
        mainGUI.textBox_status.append("Видео загружается...\n")
        mainGUI.repaint()
        path_nameVideo = mainGUI.loadVideo_pathEdit.text()
        nameVideo = str(path_nameVideo).split('/')[-1]
        pathVideo = str(path_nameVideo).split(nameVideo)[0]
        t = Thread(target=self.createMainProcessing, args=(pathVideo, nameVideo))
        t.start()
        t.join()
        mainGUI.textBox_status.append("Видео загружено!\n")
        mainGUI.settingsParameters_groupBox.setVisible(True)
