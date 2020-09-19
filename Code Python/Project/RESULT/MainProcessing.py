from RESULT.VideoProcessing import Video_Processing
from RESULT.AudioProcessing import Audio_Processing
from RESULT.training_presenter_classificator import ClassificatorPresenter


class Main_Processing:
    intervals = []

    def __init__(self, pathVideo, nameVideo):
        self.pathVideo = pathVideo
        self.nameVideo = nameVideo
        self.audioProcessing = Audio_Processing(path_video=pathVideo,
                                                name_video=nameVideo)

    def GetIntervalsPresenter(self, interval_ms):
        window_ms = self.audioProcessing.slice_ms
        margin_ms = self.audioProcessing.slice_ms
        self.classificator_presenter = ClassificatorPresenter(path_voices=self.audioProcessing.path_audio,
                                                              name_voices=self.audioProcessing.name_voices_audio,
                                                              interval_ms=interval_ms,
                                                              window_ms=window_ms,
                                                              margin_ms=margin_ms)

    def videoAnalyse(self, intervals_not_presenter, minNormalDistance, maxNormalDistance, split_interval_ms, show):
        self.videoProcessing = Video_Processing(path=self.pathVideo,
                                                name=self.nameVideo,
                                                intervals=intervals_not_presenter,
                                                interval_ms=split_interval_ms,
                                                minNormalDistance=minNormalDistance,
                                                maxNormalDistance=maxNormalDistance,
                                                show=show)

