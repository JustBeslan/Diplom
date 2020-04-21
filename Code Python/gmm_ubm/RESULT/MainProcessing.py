from RESULT.VideoProcessing import Video_Processing
from RESULT.AudioProcessing import Audio_Processing
from RESULT.training_human import HumanClassificatory


class Main_Processing:
    pathVideo = '/home/beslan/Diplom/Vebinar/'
    nameVideo = 'PartVideo2.mp4'
    pathTrain = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset2/development_set/"
    interval_presenter = [12000, 15000]

    def __init__(self, pathVideo, nameVideo, label):
        self.pathVideo = pathVideo
        self.nameVideo = nameVideo
        self.audioProcessing = Audio_Processing(pathVideo, nameVideo, label)

    def createClassificator(self, pathTrain=None, interval_presenter=None):
        humanClassificatory = HumanClassificatory(self.audioProcessing.path_audio)
        if pathTrain is not None:
            humanClassificatory.Train(pathTrain)
        else:
            interval_presenter = interval_presenter * self.audioProcessing.SR / 1000
            partDataWithPresenter = self.audioProcessing.filtered_data_audio[
                                    interval_presenter[0]: interval_presenter[1]]
            humanClassificatory.Train(x=partDataWithPresenter, sr=self.audioProcessing.SR)

    def getIntervals(self):
        self.intervals = self.audioProcessing.extract_not_presenter(self.audioProcessing.filteredPartsData)

    def videoAnalyse(self):
        # intervals = [[0, 5000], [10000, 20000]]
        interval_ms = 500
        normalDistance = 5
        videoProcessing = Video_Processing(self.pathVideo, self.nameVideo, self.intervals, interval_ms, normalDistance)
        # videoProcessing.PlayVideo()
        videoProcessing.FindConferencionRegion()
