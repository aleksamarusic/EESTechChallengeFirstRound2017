import pickle, time, random
from sklearn.ensemble import RandomForestClassifier

resenja = []
faces = 0
with open("train_data/train_label.txt") as resFile:
	for line in resFile:
		if line.startswith("1"): faces += 1
		resenja.append(int(line[:-1]))

fs = pickle.load( open("train_data/features.p", "rb") )

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
len_data = len(fs)

indexes = range(len(fs))
random.shuffle(indexes)
px = []
py = []
for ind in indexes:
	px.append(fs[ind])
	py.append(resenja[ind])
fs = px
resenja = py

training_data = fs[0:int(0.8*len_data)]      # 80% data
training_resenja = resenja[0:int(0.8*len_data)] 

testing_data = fs[int(0.8*len_data):]        # 20% data
testing_resenja = resenja[int(0.8*len_data):] 

def kinect_rdf(n_estimators, criterion, n_jobs, max_depth): 
	'''ova funkcija cita podatke(liniju po liniju), deli ih na trening i testing set,
	primenjuje rdf i sprema rdf podatke u fajl
	'''
	global training_data, training_resenja, testing_data, testing_resenja
    
	# rdf on training and testing set
	clf = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, n_jobs=n_jobs, max_depth=max_depth)
	clf.fit(training_data,training_resenja)
	clf.predict(testing_data)
	skor = clf.score(testing_data, testing_resenja)
	clf.n_classes_
	print "score: ", skor
	pickle.dump(clf, open("forest.p", "wb"))
		
	return skor
	

broj_stabala = 20
dubina_stabla = 10

print kinect_rdf(broj_stabala,'gini',2,dubina_stabla)
