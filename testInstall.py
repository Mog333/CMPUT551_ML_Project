import nltk
from nltk.book import *
from sklearn import svm


#Tests installation of NLTK and sklearn
#runs some test functions on "moby dick" (text1) 
#and runs a toy example for a svm


fdist1 = FreqDist(text1)
print(fdist1)
print("50 most common words:\n\n")
print(fdist1.most_common(50))

print("\n\nNum of times 'whale' occurs:\t%d\n\n" %fdist1['whale'])


X = [[0, 0], [1, 1]]
y = [0.2, 2.5]
clf = svm.SVR()

print(clf)

clf.fit(X, y)
p = clf.predict([[2., 2.]])
print("\nPrediction:")
print(p)
