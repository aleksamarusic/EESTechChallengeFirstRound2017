|---------------------------------------------------------|
|-----------------   Face recognition   ------------------|
|-----------   Face detection using sliding   ------------|
|---------------   window face detector   ----------------|
|---------------------------------------------------------|

By Aleksa Marusic, Nikola Pavlovic and Nikola Jovanovic

The project consists of following files:
- main.py - detects multiple faces on a large image and draws a
	bounding box arround them, it uses multi-layer-perceptron classifier
	to detect faces on parts of the image (used for task 2)
- the classes/functions in featureExtractor.py are used to generate features
 	from an image or a part of image
- classify.py does the classification of the images in test data set and generates
	the labels (task 2)
- train_SGD.py trains the stochastic gradient descent classifier used in classify.py
	during development, it was shown that MLP was better for multi-face detection
	and SGD proved better for the first task


