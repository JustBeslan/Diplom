import numpy as np
import os
import cv2

def prizn_im(path):
	image = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
	image_96 = cv2.resize(image,(image.shape[1],image.shape[0]))

#	cv2.imshow('res',image_96)
#	cv2.waitKey(0)

	countNonZero_im_96 = cv2.countNonZero(image_96)
#	print(countNonZero_im_96)

	R1 = image_96[0:image_96.shape[1], 0:int(image_96.shape[0]/3)]
	R1 = cv2.countNonZero(R1)/countNonZero_im_96

	R2 = image_96[0:image_96.shape[1], int(image_96.shape[0]/3):2*int(image_96.shape[0]/3)]
	R2 = cv2.countNonZero(R2)/countNonZero_im_96

	R3 = image_96[0:image_96.shape[1], 2*int(image_96.shape[0]/3):image_96.shape[0]]
	R3 = cv2.countNonZero(R2)/countNonZero_im_96

	R4 = image_96[0:int(image_96.shape[1]/3), 0:image_96.shape[0]]
	R4 = cv2.countNonZero(R4)/countNonZero_im_96

	R5 = image_96[int(image_96.shape[1]/3):2*int(image_96.shape[1]/3), 0:image_96.shape[0]]
	R5 = cv2.countNonZero(R5)/countNonZero_im_96

	R6 = image_96[2*int(image_96.shape[1]/3):image_96.shape[1], 0:image_96.shape[0]]
	R6 = cv2.countNonZero(R6)/countNonZero_im_96

	GR = countNonZero_im_96/(image_96.shape[0]*image_96.shape[1])

	WHR = image_96.shape[1]/image_96.shape[0]

	return np.array([R1,R2,R3,R4,R5,R6,GR,WHR])


path_dir = "/home/beslan/fonts/fonts png/Old"
arr_all_dir = os.listdir(path_dir)
used_dir = np.zeros(len(arr_all_dir))
print(len(arr_all_dir))

for i in range(0,len(arr_all_dir)):
	rand_Ndir = np.random.randint(0,len(arr_all_dir)-1)
	if used_dir[rand_Ndir] == 1:
		while used_dir[rand_Ndir] == 1: 
			rand_Ndir = np.random.randint(0,len(arr_all_dir)-1)
	else:
		used_dir[rand_Ndir] == 1
	print(arr_all_dir[rand_Ndir])

	arr_all_files = os.listdir(path_dir + "/" + arr_all_dir[rand_Ndir])
	print(len(arr_all_files))
	
	rand_Nfile = np.random.randint(0,len(arr_all_files)-1)

	print(arr_all_files[rand_Nfile])
	a = prizn_im(path_dir + "/" + arr_all_dir[rand_Ndir] + "/" + arr_all_files[rand_Nfile])
	print(a)

