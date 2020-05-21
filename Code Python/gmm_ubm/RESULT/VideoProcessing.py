import cv2 as cv
import pytesseract
import dlib

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
TESSDATA_PREFIX = 'C:/Program Files/Tesseract-OCR'


class Video_Processing:
    intervals_together = []
    intervals_someone = []
    interval = []

    def __init__(self, path, name, intervals, interval_ms, minNormalDistance, maxNormalDistance, show):
        self.video = cv.VideoCapture(path + name)
        self.intervals = intervals
        self.interval_ms = interval_ms
        self.minNormalDistance = minNormalDistance
        self.maxNormalDistance = maxNormalDistance
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(path + 'shape_predictor_68_face_landmarks.dat')
        self.show = show
        countFrame = int(self.video.get(cv.CAP_PROP_FRAME_COUNT))
        fps = int(self.video.get(cv.CAP_PROP_FPS))
        self.timeVideo = countFrame / fps
        print("time video (sec) = ", self.timeVideo)
        if len(intervals) > 0:
            self.FindConferencionRegion()

    def PlayVideo(self):
        while self.video.isOpened():
            ret, frame = self.video.read()

            if ret:
                cv.imshow('Video', frame)
                if cv.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        self.video.release()
        cv.destroyAllWindows()

    def FindConferencionRegion(self):
        print(self.intervals)
        print(self.interval_ms)
        i = 0
        j = 0
        b = True
        while self.video.isOpened():

            time_from = self.intervals[i][0] + j * self.interval_ms
            self.video.set(cv.CAP_PROP_POS_MSEC, time_from)
            ret, frame = self.video.read()

            time_to = time_from + self.interval_ms
            if time_to >= self.intervals[i][1]:
                time_to = self.intervals[i][1]
                i += 1
                b = True
                j = 0
                if i == len(self.intervals):
                    break
            self.video.set(cv.CAP_PROP_POS_MSEC, time_to)
            ret2, frame2 = self.video.read()
            self.interval = [time_from, time_to]

            if ret and ret2:
                minutesVideo = int(self.video.get(cv.CAP_PROP_POS_MSEC) / 1000) / 60
                if minutesVideo % 5 == 0 or b:
                    self.GetConferencionRegion(frame)
                    b = False
                self.AnalyzeConferencionRegion(frame, frame2)
                if cv.waitKey(25) & 0xFF == ord('q'):
                    break
                j += 1
            else:
                break
        self.video.release()
        cv.destroyAllWindows()

    def GetConferencionRegion(self, img):
        ret2, threshold = cv.threshold(src=img,
                                       thresh=250,
                                       maxval=255,
                                       type=cv.THRESH_BINARY)
        hsv = cv.cvtColor(src=threshold,
                          code=cv.COLOR_BGR2HSV)
        canny = cv.Canny(hsv, 10, 527)
        image, contours, hierarchy = cv.findContours(image=canny,
                                                     mode=cv.RETR_EXTERNAL,
                                                     method=cv.CHAIN_APPROX_SIMPLE)
        imagesTitles = []
        for contour in contours:
            minAreaRect = cv.minAreaRect(points=contour)
            if minAreaRect[1][0] >= 80 and minAreaRect[1][1] >= 80:
                titleY = minAreaRect[0][1] - minAreaRect[1][1] / 2 - 20
                imagesTitles.append([img[int(titleY - 10):int(titleY + 20),
                                     int(minAreaRect[0][0] - minAreaRect[1][0] / 2):int(
                                         minAreaRect[0][0] + minAreaRect[1][0] / 2)], minAreaRect])
        for i in range(len(imagesTitles)):
            if imagesTitles[i][0].shape[0] > 0 and imagesTitles[i][0].shape[1] > 0:
                title = self.GetTextTitle(img=imagesTitles[i][0])
                if title == "Конференция":
                    self.regionConferencion = imagesTitles[i][1]

    def GetTextTitle(self, img):
        listImageTitleShape = list(img.shape)
        listImageTitleShape = [listImageTitleShape[1] * 3, listImageTitleShape[0] * 4]
        resizedImg = cv.resize(src=img,
                               dsize=tuple(listImageTitleShape))
        grayImg = cv.cvtColor(src=resizedImg,
                              code=cv.COLOR_BGR2GRAY)
        ret, binaryImg = cv.threshold(src=grayImg,
                                      thresh=127,
                                      maxval=255,
                                      type=cv.THRESH_BINARY)
        return pytesseract.image_to_string(image=binaryImg,
                                           lang='rus')

    def GetCoordinatesXYFromShape(self, shape):
        Coordinates = []
        for i in range(0, 68):
            Coordinates.append((shape.part(i).x, shape.part(i).y))
        return Coordinates

    def GetDistanceBetweenPoints(self, point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

    def AnalyzeConferencionRegion(self, img1, img2):
        regionConferencionPoint1 = [self.regionConferencion[0][i] - self.regionConferencion[1][i] / 2 for i in
                                    range(0, len(self.regionConferencion[0]))]
        regionConferencionPoint2 = [regionConferencionPoint1[i] + list(self.regionConferencion[1])[i] for i in
                                    range(0, len(regionConferencionPoint1))]

        image1RegionConferencion = img1[int(regionConferencionPoint1[1]):int(regionConferencionPoint2[1]),
                                   int(regionConferencionPoint1[0]):int(regionConferencionPoint2[0])]
        image2RegionConferencion = img2[int(regionConferencionPoint1[1]):int(regionConferencionPoint2[1]),
                                   int(regionConferencionPoint1[0]):int(regionConferencionPoint2[0])]

        faces1 = self.detector(image1RegionConferencion)
        faces2 = self.detector(image2RegionConferencion)

        if len(faces1) + len(faces2) > 0:
            if len(faces1) == 0 or len(faces2) == 0:
                # print("Presenter not say")
                self.intervals_someone.append(self.interval)
            else:
                face1Presenter = faces1[0]
                face2Presenter = faces2[0]
                shape1 = self.predictor(image1RegionConferencion, face1Presenter)
                shape2 = self.predictor(image2RegionConferencion, face2Presenter)
                Coordinates1 = self.GetCoordinatesXYFromShape(shape1)
                Coordinates2 = self.GetCoordinatesXYFromShape(shape2)
                distances = []
                for i in range(49, len(Coordinates1) - 1):
                    distance = self.GetDistanceBetweenPoints(Coordinates1[i], Coordinates2[i])
                    distances.append(distance)
                check_say_presenter = [distance for distance in distances
                                       if self.minNormalDistance <= distance <= self.maxNormalDistance]
                if len(check_say_presenter) < len(distances) // 2:
                    # print("Presenter not say")
                    self.intervals_someone.append(self.interval)
        else:
            # print("Presenter is not found")
            self.intervals_someone.append(self.interval)
        if self.show:
            cv.imshow('Video', image1RegionConferencion)
