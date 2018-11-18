import numpy as np
import cv2
import sys 
import pickle

from featureExtractor import ekstractFeatures as ef

IMG_SIZE = 48
# -1 for all
IMGS_TO_LOAD = -1
# "demo_data/"; "train_data/"; "test_data/"
TRAIN_DATA_FOLDER = "test_data/" 

imgList = []
imgListFile = open(TRAIN_DATA_FOLDER + "train_image.txt")
for line in imgListFile: imgList.append(line[:-1])
imgListFile.close()

features = []
co = 0
for img in imgList:
	inimg = cv2.resize(
		cv2.imread(TRAIN_DATA_FOLDER + "train/" + img, cv2.IMREAD_GRAYSCALE), 
		(IMG_SIZE, IMG_SIZE))
	# cv2.equalizeHist(inimg, inimg)
	features.append(ef(inimg, IMG_SIZE))
	co += 1
	if co & 15 == 0:
		print "\r", co
	if (co == IMGS_TO_LOAD): break
	
pickle.dump( features, open( TRAIN_DATA_FOLDER + "/features.p", "wb" ) )

