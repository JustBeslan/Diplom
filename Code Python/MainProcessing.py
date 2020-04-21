from VideoProcessing import Video_Processing
from AudioProcessing import Audio_Processing
from Clustering2 import Clustering2_

#---------Attempt2------------------
path = '/home/beslan/Diplom/Test5/Audio/'
name = 'Audiotest5.wav'
slice_ms = 500
clustering2 = Clustering2_(path,name,slice_ms)

#-------------------------------Video----------------------------------
# path = '/home/beslan/Diplom/Vebinar/'
# name = 'PartVideo2.mp4'
# intervals = [[0,5000],[10000,20000]]
# interval_ms = 500
# normalDistance = 5
# videoProcessing = Video_Processing(path,name,intervals,interval_ms,normalDistance)
# videoProcessing.PlayVideo()
# videoProcessing.FindConferencionRegion()
#-----------------------------Audio--------------------------------
# path = "/home/beslan/Diplom/Test1/"
# name = "test0.mp4"

# pathAudio = "/home/beslan/Diplom/Test4/Audio/"
# nameAudio = "Audiotest4.wav"

# audioProcessing = Audio_Processing(pathAudio,nameAudio)
# # audioProcessing.ToExtractAudioFromVideo()
# audioProcessing.Processing()
