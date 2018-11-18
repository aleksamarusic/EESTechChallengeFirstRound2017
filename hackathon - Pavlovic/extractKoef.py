import numpy as np
import cv2
import feature_extractor as fe
import os

# 'training_set' or 'validation_set'
path = 'validation_set'

faceCascPath = 'haarcascade_frontalface_alt.xml'
eyeCascPath  = 'haarcascade_eye.xml'
mouthCascadePath = 'haarcascade_mouth.xml'
faceCascade = cv2.CascadeClassifier(faceCascPath)
eyeCascade = cv2.CascadeClassifier(eyeCascPath)
mouthCascade = cv2.CascadeClassifier(mouthCascadePath)

files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
for f in files:
    if f.endswith('.png'):
        img = cv2.imread(path + '/' +  f)
        features = fe.extract_features(img, faceCascade, eyeCascade, mouthCascade)
        if features[0] == False:
            continue
        text = ''
        for koef in features[2:]:
            text += str(koef) + ' '
        cv2.imshow(str(f), features[1]) # iscrtavanje svih slika iz seta
        with open(path + '\\' + path + '.txt', 'a') as file:
            file.write(f[-5] + ' ' + text + '\n')

print ('Extraction completed')

while (True):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows() # potrebno ukoliko je omoguceno iscrtavanje slika iz seta

