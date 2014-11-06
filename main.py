#! /usr/bin/env python


import numpy as np
from sklearn import svm
import time


def preProcess(words):
   words = words.replace('  ', ' ')
   words = words.replace(',', "")
   words = words.replace('.', '')
   words = words.replace('!', '')
   words = words.replace('\'', '')
   words = words.replace('\"', '')
   words = words.replace('\n', '')
   return words


t0 = time.time()


in_file = open("tweet.txt", 'r')

words = []

first = 0
numRows = 0
for line in in_file:
   line = preProcess(line)
   newWords = line.split(' ')
   words = words + newWords
   numRows += 1



#words = preProcess(words)


all_words = words
all_words_lower = []
# make sure every word is lower case. Smart thing to do in general??
for word in all_words:
   all_words_lower.append(word.lower())

all_words = all_words_lower

# now that all the words have been parsed, we make a dictionary
# with key = word, value = index in a feature vector

bag_dict = {}

featureWords = []

counter_unique = 0
counter_total = 0
for word in all_words:
   counter_total = counter_total + 1

   if word in bag_dict:
      continue
   else:
      bag_dict[word] = counter_unique
      counter_unique = counter_unique + 1
      #featureWords.append(word) # featureWords only contains each word once



#featureMatrix = np.zeros((numRows, counter_unique))
featureMatrix = []


in_file.seek(0,0)
lineCount = 0
for line in in_file:
 
   tweet = preProcess(line)
   tweetList = tweet.split(' ')

   #print(tweetList)
   featureVec = np.zeros(counter_unique)
   for word in tweetList:
      word = word.lower()
      #print(word)
      index = bag_dict[word]
      featureVec[index] += 1
   lineCount += 1
   featureMatrix.append(featureVec)  

#print bag_dict

#print words

print("=====================")
in_file.close()

#print(bag_dict)


print("total number of words = " + str(counter_total))
print("total number of unique words = " + str(counter_unique))

X = np.array(featureMatrix)
#print(X)



t1 = time.time()


print("Time to create feature vectors = " + str(t1-t0))
''' NOW TRAIN SVM!!!!! '''


t0 = time.time()

in_labels = open("score.txt", 'r')

scores = []

for line in in_labels:
   #print(line)
   line = line.replace('\n', '')
   scores.append(line)

#print(scores)

Y = np.array(scores)

#print(Y)
clf = svm.SVR()

#print(clf)

clf.fit(X, Y)

t1 = time.time()



print("Time to train SVM = " + str(t1-t0))

'''
#testPoint is the tweet "Adam Sankalp 
testPoint = np.zeros(counter_unique)
testPoint[58] = 1
testPoint[59] = 1
p = clf.predict(testPoint)
print("\nPrediction 'Adam Sankalp':")
print(p)


#testPoint2 is the tweet "I like Adam and Sankalp" 
testPoint2 = np.zeros(counter_unique)
testPoint2[1] = 1
testPoint2[18] = 1
testPoint2[57] = 1
testPoint2[58] = 1
testPoint2[59] = 1
p = clf.predict(testPoint2)
print("\nPrediction 'I like Adam and Sankalp':")
print(p)
'''

# testPoint is the tweet "working for 6.5 hours" 
testPoint3 = np.zeros(counter_unique)
testPoint3[3] = 1
testPoint3[4] = 1
testPoint3[5] = 1
testPoint3[6] = 1
p = clf.predict(testPoint3)
print("\nPrediction 'working for 6.5 hours':")
print(p)





