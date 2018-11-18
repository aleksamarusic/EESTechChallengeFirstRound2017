import pickle
from featureExtractor import ekstractFeatures as ef

class Forest:
	def __init__(self):
		self.forest = pickle.load( open("forest.p", "rb") )
	def classify(self, features):
		return self.forest.predict([features])
		
class SGD:
	def __init__(self):
		self.sgd = pickle.load( open("SGD.p", "rb") )
	def classify(self, features):
		return self.sgd.predict([features])
	
if __name__ == "__main__":
	import cv2
	IMG_SIZE = 48
	
	print "Loading classifier"
	# SGD(); Forest()
	classifier = SGD()
	print "Loading picture"
	
	img = cv2.resize(
		cv2.imread("2.jpg", cv2.IMREAD_GRAYSCALE),
		(IMG_SIZE, IMG_SIZE))
	cv2.imshow("img", img)
	print "Clasification"
	print classifier.classify(ef(img, IMG_SIZE))
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	while True:
		try:
			i = input()
			img = cv2.resize(
				cv2.imread("train_data/train/"+str(i)+".jpg", cv2.IMREAD_GRAYSCALE),
				(IMG_SIZE, IMG_SIZE))
			cv2.imshow("img", img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			print classifier.classify(ef(img, IMG_SIZE))
		except:
			pass