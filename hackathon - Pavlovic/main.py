import pickle

from featureExtractor import ekstractFeatures
from hiatogram_filter import hist_filter

classifier = None
try:
    clsf = open("classifier.pickle", "r")
    classifier = pickle.load(clsf)
    clsf.close()
except:

    file = open("features.p")
    nizovi = pickle.load(file)
    print len(nizovi[0]), len(nizovi[1])
    labels = []
    for label in open("train_label.txt"):
        labels.append(int(label.strip()))
    labels = labels[:len(nizovi)]
    import nltk
    import sklearn
    import sklearn.ensemble
    from sklearn.neural_network import MLPClassifier

    classifier = MLPClassifier(hidden_layer_sizes=(500), alpha=0.001)

    classifier.fit(nizovi, labels)
    clsf = open("classifier.pickle", "w")
    pickle.dump(classifier, clsf)
    clsf.close()

import cv2

SIZE_LOW = 30
SIZE_HIGH = 300
SHIFT_COEFF = 0.1

SCALE_TO = 48


def calc_features(submatrix):
    return ekstractFeatures(submatrix, SCALE_TO)


def get_features(submatrix):
    resized = cv2.resize(submatrix.copy(), (SCALE_TO, SCALE_TO))
    return calc_features(resized)


def is_face(features):
    return classifier.predict_proba([features])[0][1]


def area(a, b):  # returns None if rectangles don't intersect
    dx = min(a[2], b[2]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[1], b[1])
    if (dx >= 0) and (dy >= 0):
        return dx * dy
    else:
        return 0.0


def rectarea(r):
    return abs(r[0] - r[2]) * abs(r[1] - r[3])


def push_rect(rects, rect):
    for i in range(len(rects)):
        if area(rects[i][0], rect[0]) > rectarea(rects[i][0])*0.2:
            if rects[i][1] < rect[1]:
                rects[i] = rect
            return
    rects.append(rect)


def run_for_patches(image):
    global colorpicture
    h = len(image)
    w = len(image[0])
    faces = []
    c = 0
    rects = []
    for size in range(SIZE_LOW, SIZE_HIGH + 1):
        print size
        shift = int(size * SHIFT_COEFF)
        for i in range(0, h, shift):
            print i
            if i + size > h:
                break
            tests = []
            for j in range(0, w, shift):
                if j + size > w:
                    break
                tested = image.copy()[i:i + size, j:j + size]
                # tests.append(tested)

                if hist_filter(cv2.resize(tested, (SCALE_TO, SCALE_TO))):
                    features = get_features(tested)
                    yes = is_face(features)
                    if yes > 0.7:
                        rect=((j,i,j+size,i+size),yes)
                        push_rect(rects, rect)
        if len(rects)>0:
            break
    for rect in rects:
        rect=rect[0]
        cv2.rectangle(colorpicture, (rect[0],rect[1]),(rect[2], rect[3]), (255, 0, 0), 3)
    cv2.imwrite("rezultat.jpg", colorpicture)

    return faces

IMAGE_PATH = "12.jpg"

picture = cv2.imread(IMAGE_PATH, cv2.CV_LOAD_IMAGE_GRAYSCALE)
cv2.equalizeHist(picture, picture)
colorpicture = cv2.imread(IMAGE_PATH, 1)
run_for_patches(picture)