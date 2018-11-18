import pickle, random
from sklearn.linear_model import SGDClassifier

print "Reading Y"
resenja = []
faces = 0
with open("train_data/train_label.txt") as resFile:
	for line in resFile:
		if line.startswith("1"): faces += 1
		resenja.append(int(line[:-1]))

print "Reading X"
fs = pickle.load( open("train_data/features.p", "rb") )
print "Features", len(fs[0])
# randomize order
indexes = range(len(fs))
random.shuffle(indexes)
px = []
py = []
for ind in indexes:
	px.append(fs[ind])
	py.append(resenja[ind])
fs = px
resenja = py


""" balancing positive and negative training examples 
ind = 0
nonFaces = 0
while ind < len(resenja):
	if nonFaces < faces:
		if resenja[ind] == 0: nonFaces += 1
	else:
		if resenja[ind] == 0:
			del resenja[ind]
			del fs[ind]
			ind -= 1
	ind += 1
# randomize order
indexes = range(len(fs))
random.shuffle(indexes)
px = []
py = []
for ind in indexes:
	px.append(fs[ind])
	py.append(resenja[ind])
fs = px
resenja = py """
	
len_data = len(fs)

training_data = fs[0:int(0.8*len_data)]      # 80% data
training_resenja = resenja[0:int(0.8*len_data)] 
print "Training", len(training_data), len(training_resenja)

testing_data = fs[int(0.8*len_data):]        # 20% data
testing_resenja = resenja[int(0.8*len_data):] 
print "Test", len(testing_data), len(testing_resenja)

print "Training"
clf = SGDClassifier(loss='hinge', alpha = 0.001, n_iter=2000,
	penalty='l2', shuffle=True).fit(training_data, training_resenja)

pickle.dump(clf, open("SGD.p", "wb"))

#preds = clf.predict_proba(testing_data)
preds = clf.predict(testing_data)
print type(preds[0]), preds
print type(testing_resenja[0]), testing_resenja
tp = 0
tn = 0
fp = 0
fn = 0
for i in range(len(testing_data)):
	if (preds[i] == 1) and (preds[i] == testing_resenja[i]): tp += 1
	elif (preds[i] == 1) and (preds[i] != testing_resenja[i]): fp += 1
	elif (preds[i] != 1) and (preds[i] == testing_resenja[i]): tn += 1
	elif (preds[i] != 1) and (preds[i] != testing_resenja[i]): fn += 1

print tp, tn, fp, fn


