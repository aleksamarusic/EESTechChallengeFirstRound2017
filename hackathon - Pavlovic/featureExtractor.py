import numpy as np
import cv2, pickle

NUM_OF_MASKS = 5
PAIRS_TO_USE = 1000

masks = [{} for i in range(NUM_OF_MASKS)]
maskSizes = [4, 8, 16]
# mask 1
for s in maskSizes:
	masks[0][s] = np.ones((s, s))
	for i in range(s/2, s):
		for j in range(s):
			masks[0][s][j,i] = -1
# mask 2
for s in maskSizes:
	masks[1][s] = np.ones((s, s))
	for i in range(s):
		for j in range(s/2):
			masks[1][s][j,i] = -1
# mask 3
for s in maskSizes:
	masks[2][s] = np.ones((s, s))
	for i in range(s):
		for j in range(s):
			if (j > s / 4) and (j < 3 * s / 4): masks[2][s][j,i] = -1
# mask 4
for s in maskSizes:
	masks[3][s] = np.ones((s, s))
	for i in range(s):
		for j in range(s):
			if (i > s / 4) and (i < 3 * s / 4): masks[3][s][j,i] = -1
# mask 5
for s in maskSizes:
	masks[4][s] = np.ones((s, s))
	for i in range(s):
		for j in range(s):
			if ((j < s / 2) and (i < s / 2)) or \
				(j > s / 2) and (i > s / 2): masks[4][s][j,i] = -1
# mask 6
"""for s in maskSizes:
	masks[5][s] = np.ones((s, s))
	for i in range(s):
		for j in range(s):
			if (j < s / 4) or (i < s / 4) or \
				(j > 3 * s / 4) or (i > 3 * s / 4): masks[5][s][j,i] = -2/3.0
			else: masks[5][s][j,i] = 2"""
			
pairs = pickle.load(open("pairs.p", "rb"))

def ekstractFeatures(img, size):
	features = []
	for patchSize in maskSizes:
		area = patchSize * patchSize
		for x in range(0, size, patchSize):
			for y in range(0, size, patchSize):
				patch = img[y : y+patchSize, x : x+patchSize]
				for m in range(NUM_OF_MASKS):
					features.append(float(np.tensordot(patch, masks[m][patchSize])) / area / 128.0)
	features = features + \
		(img.sum(axis=0) / size / 256.0).tolist() + \
		(img.sum(axis=1) / size / 256.0).tolist()
	for p in pairs[:PAIRS_TO_USE]:
		features.append(features[p[0]] * features[p[1]] * 4)
	return features

