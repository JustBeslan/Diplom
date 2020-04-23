from RESULT.VideoProcessing import Video_Processing
from RESULT.AudioProcessing import Audio_Processing
from RESULT.training_human import HumanClassificatory
from tkinter import END
import numpy as np
import librosa


class Main_Processing:
    pathVideo = '/home/beslan/Diplom/Vebinar/'
    nameVideo = 'PartVideo2.mp4'
    pathTrain = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset2/development_set/"
    interval_presenter = [12000, 15000]

    def __init__(self, pathVideo, nameVideo, messages):
        self.pathVideo = pathVideo
        self.nameVideo = nameVideo
        self.messages = messages
        self.audioProcessing = Audio_Processing(pathVideo, nameVideo, messages)

    def createClassificator(self, is_presenter, path_train, interval_presenter=None):
        humanClassificatory = HumanClassificatory(self.audioProcessing.path_audio)
        if not is_presenter:
            self.messages.insert(END, "Идет создание классификатора остальных участников...\n")
            humanClassificatory.Train(is_presenter=is_presenter, path_train_data=path_train)
            self.messages.insert(END, "Создан классификатор остальных участников...\n")
        else:
            self.messages.insert(END, "Идет создание классификатора ведущего...\n")
            interval_presenter = self.audioProcessing.SR * (np.array(interval_presenter) // 1000)
            # partDataWithPresenter = self.audioProcessing.filtered_data_audio[
            #                         interval_presenter[0]: interval_presenter[1]]
            partDataWithPresenter = self.audioProcessing.filteredPartsData.flatten()[
                                    interval_presenter[0]: interval_presenter[1]]
            librosa.output.write_wav(self.audioProcessing.path_audio + "Part" + self.audioProcessing.nameFilteredAudio,
                                     partDataWithPresenter, self.audioProcessing.SR)
            humanClassificatory.Train(is_presenter=is_presenter, path_train_data=path_train,
                                      x=partDataWithPresenter, sr=self.audioProcessing.SR)
            self.messages.insert(END, "Создан классификатор ведущего...\n")

    def getIntervals(self):
        self.intervals = self.audioProcessing.extract_not_presenter(self.audioProcessing.filteredPartsData)

    def videoAnalyse(self):
        # intervals = [[0, 5000], [10000, 20000]]
        interval_ms = 500
        normalDistance = 5
        videoProcessing = Video_Processing(self.pathVideo, self.nameVideo, self.intervals, interval_ms, normalDistance)
        # videoProcessing.PlayVideo()
        videoProcessing.FindConferencionRegion()
