import numpy as np
import cv2
import sys
import os

NUM_OF_patchS = 5

masks = [{} for i in range(5)]
maskSizes = [4, 5, 8, 10, 20, 40, 25, 50, 100]
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
			


def ekstractFeatures(img, size, patchSizes):
	features = []
	for patchSize in patchSizes:
		for x in range(0, size, patchSize):
			for y in range(0, size, patchSize):
				patch = img[y : y+patchSize, x : x+patchSize]
				# sums = [0 for i in range(NUM_OF_patchS)]
				for m in range(5):
					features.append(float(np.tensordot(patch, masks[m][patchSize])))
				"""
				for i in range(patchSize):
					for j in range(patchSize):
						# mask 1
						if i < patchSize / 2: sums[0] += patch[j,i]
						else: sums[0] -= patch[j,i]
						# mask 2
						if j < patchSize / 2: sums[1] += patch[j,i]
						else: sums[1] -= patch[j,i]
						# mask 3
						if (j < patchSize / 4) or (j > 3 * patchSize / 4): sums[2] += patch[j][i]
						else: sums[2] -= patch[j][i]
						# mask 4
						if (i < patchSize / 4) or (i > 3 * patchSize / 4): sums[3] += patch[j][i]
						else: sums[3] -= patch[j][i]
						# mask 5
						if ((j < patchSize / 2) and (i < patchSize / 2)) or \
							(j > patchSize / 2) and (i > patchSize / 2): sums[4] += patch[j][i]
						else: sums[4] -= patch[j][i]
				"""
				# for i in range(NUM_OF_patchS): features.append(sums[i])
	return features



"""
im2, contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
consimg = np.zeros((256,256), np.uint8)
cv2.drawContours(consimg, contours, -1, (100,255,100), 3)
cv2.imshow("conts", consimg)

while min([cv2.contourArea(cont) for cont in contours]) < 40:
	minconti = [cv2.contourArea(cont) for cont in contours].index(min([cv2.contourArea(cont) for cont in contours]))
	del contours[minconti]
	
gridi = [cv2.arcLength(cont,True) for cont in contours].index(max([cv2.arcLength(cont,True) for cont in contours]))
del contours[gridi]
squarei = [cv2.contourArea(cont) for cont in contours].index(max([cv2.contourArea(cont) for cont in contours]))

consimg = np.zeros((256,256), np.uint8)
cv2.drawContours(consimg, contours, -1, (100,255,100), 3)
go = 255
do = 0
le = 255
de = 0
for point in contours[squarei]:
	po = point[0]
	if (po[0] < le): le = po[0] 
	if (po[0] > de): de = po[0] 
	if (po[1] < go): go = po[1]
	if (po[1] > do): do = po[1]

del contours[squarei]

cv2.line(consimg, (le, 0), (le,255), (200, 200, 200))
cv2.line(consimg, (de, 0), (de,255), (200, 200, 200))
cv2.line(consimg, (0,go), (255,go), (200, 200, 200))
cv2.line(consimg, (0,do), (255,do), (200, 200, 200))
cv2.imshow("conts -grid", consimg)

brects = [(cv2.boundingRect(cont)) for cont in contours] #  x,y,w,h =

todeli = []
for i in range(len(contours)):
	for j in range(i+1, len(contours)):
		if (brects[i][0] < brects[j][0]) and (brects[i][1] < brects[j][1]) and (brects[i][0]+brects[i][2] > brects[j][0]+brects[j][2]) and (brects[i][1]+brects[i][3] > brects[j][1]+brects[j][3]):
			todeli.append(j)
		if (brects[j][0] < brects[i][0]) and (brects[j][1] < brects[i][1]) and (brects[j][0]+brects[j][2] > brects[i][0]+brects[i][2]) and (brects[j][1]+brects[j][3] > brects[i][1]+brects[i][3]):
			todeli.append(i)
for i in todeli[::-1]:
	del contours[i]
	
print "Contours: ", len(contours)

consimg = np.zeros((256,256), np.uint8)
cv2.drawContours(consimg, contours, -1, (100,255,100), 3)
brects = [(cv2.boundingRect(cont)) for cont in contours] #  x,y,w,h = 
for rect in brects:
	cv2.rectangle(consimg,(rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]),(50,255,200),1)
cv2.line(consimg, (le, 0), (le,255), (200, 200, 200))
cv2.line(consimg, (de, 0), (de,255), (200, 200, 200))
cv2.line(consimg, (0,go), (255,go), (200, 200, 200))
cv2.line(consimg, (0,do), (255,do), (200, 200, 200))
cv2.imshow("rects", consimg)

averagearea = sum([cv2.contourArea(cont) for cont in contours]) / len(contours)
	
table = [["-" for i in range(3)] for j in range(3)]

for i in range(len(contours)):
	midx = brects[i][0] + brects[i][2]/2
	midy = brects[i][1] + brects[i][3]/2
	c = 'X'
	if cv2.contourArea(contours[i]) > averagearea: c = 'O'
	if (midx < le) and (midy < go): table[0][0] = c
	elif (midx < le) and (midy > do): table[2][0] = c
	elif (midx < le): table[1][0] = c
	
	elif (midx < de) and (midy < go): table [0][1] = c
	elif (midx < de) and (midy > do): table [2][1] = c
	elif (midx < de): table[1][1] = c
	
	elif (midy < go): table[0][2] = c
	elif (midy > do): table[2][2] = c
	else: table[1][2] = c
	

cv2.waitKey(0)
cv2.destroyAllWindows()
"""