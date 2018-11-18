import cv2

SHOW = 0

resenja = []
faces = 0
with open("train_data/train_label.txt") as resFile:
	for line in resFile:
		if line.startswith("1"): faces += 1
		resenja.append(int(line[:-1]))
		
with open("train_data/train_image.txt") as inFile:
	co = 0
	for line in inFile:
		if resenja[co] == SHOW:
			img = cv2.imread("train_data/train/" + line[:-1], 1)
			cv2.imshow("img", img)
			print co
			cv2.waitKey(0)
		co += 1