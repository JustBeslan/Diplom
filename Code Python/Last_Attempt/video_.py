import numpy as np
import cv2
import dlib
import argparse
from imutils import face_utils
import sys

def x_y(shape_):
	x_ = []
	y_ = []
	for i in range(0,68):
		x_.append(shape_.part(i).x)
		y_.append(shape_.part(i).y)
	return x_,y_

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('/home/beslan/dlib-19.17.0/shape_predictor_68_face_landmarks.dat')

path_video = '/home/beslan/video3_1.mp4'
cap = cv2.VideoCapture(0)
while cap.isOpened():
	ret,frame = cap.read()

	faces = detector(frame,0)
	print(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)

	if len(faces) > 0:
		r = faces[0]	
		cv2.rectangle(frame,(r.left(),r.top()),(r.right(),r.bottom()),(255,0,0),1)

		shape = predictor(frame, r)
		x,y = x_y(shape)
		print(len(x))
#		print(x)

		if len(x) > 0:
			for i in range(48,len(x)-1):
	#			print(shape.part(i).x,shape.part(i).y)
				cv2.circle(frame,(x[i],y[i]),2,(255,0,0),0)
				cv2.line(frame,(x[i],y[i]),(x[i+1],y[i+1]),(0,0,255))
#			cv2.line(frame,(x[len(x)-1],y[len(x)-1]),(x[len(x)],y[len(x)]),(0,0,255))

	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		breakq
cap.release()
cv2.destroyAllWindows()