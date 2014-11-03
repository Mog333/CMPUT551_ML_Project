#! /usr/bin/env python


import numpy as np
from sklearn import svm



def main():   
   tws = getTweetsFromFile("tweet.txt")
   scoreColumn = getTweetScoresFromFile("score.txt")
   d = buildBOWDictFromTweets(tws)
   fm = getFeatureMatrix(tws, d)
   clf = svm.SVR()
   clf.fit(fm, scoreColumn)
   print("Done fitting")
   return (tws, scoreColumn, d, clf)

def preProcess(words):
   words = words.replace('  ', ' ')
   words = words.replace(',', "")
   words = words.replace('.', '')
   words = words.replace('!', '')
   words = words.replace('\'', '')
   words = words.replace('\"', '')
   words = words.replace('\n', '')
   return words
   

def getTweetsFromFile(filename):
   input_file = open(filename, 'r')
   tweets = []
   for line in input_file:
      tweets.append(preProcess(line.lower()))
   input_file.close()
   return tweets


def buildBOWDictFromTweets(tweetList):
   bow_dict = {}
   number_unique_words = 0
   for tweet in tweetList:
      for word in tweet.split(" "):
         if word in bow_dict:
            continue
         else:
            bow_dict[word] = number_unique_words
            number_unique_words += 1
   return bow_dict

def getFeatureVec(tweet, bow_dict):
   featureVec = np.zeros(len(bow_dict))
   for word in tweet.split(" "):
      try:
         index = bow_dict[word]
         featureVec[index] += 1
      except KeyError:
         continue
   return featureVec

def getFeatureMatrix(tweetList, bow_dict):
   featureMatrix = getFeatureVec(tweetList[0], bow_dict)
   
   for tweet in tweetList[1:]:
      v = getFeatureVec(tweet, bow_dict)
      featureMatrix = np.vstack([featureMatrix, v])

   return featureMatrix

def getTweetScoresFromFile(filename):
   input_file = open(filename, 'r')
   tweetScores = np.array([])
   for line in input_file:
      score = float(line.lower().replace("\n", ""))
      tweetScores = np.append(tweetScores, score)
   input_file.close()
   return np.transpose(tweetScores)


#in_labels = open("small_score.txt", 'r')

#scores = []

#for line in in_labels:
#   print(line)
#   line = line.replace('\n', '')
#   scores.append(line)

#print(scores)

#Y = np.array(scores)

#print(Y)
#clf = svm.SVR()

#print(clf)

#clf.fit(X, Y)


''' testPoint is the tweet "Adam Sankalp" '''
#testPoint = np.zeros(counter_unique)
#testPoint[58] = 1
#testPoint[59] = 1
#p = clf.predict(testPoint)
#print("\nPrediction 'Adam Sankalp':")
#print(p)


''' testPoint2 is the tweet "I like Adam and Sankalp" '''
#testPoint2 = np.zeros(counter_unique)
#testPoint2[1] = 1
#testPoint2[18] = 1
#testPoint2[57] = 1
#testPoint2[58] = 1
#testPoint2[59] = 1
#p = clf.predict(testPoint2)
#print("\nPrediction 'I like Adam and Sankalp':")
#print(p)


''' testPoint is the tweet "working for 6.5 hours" '''
#testPoint3 = np.zeros(counter_unique)
#testPoint3[3] = 1
#testPoint3[4] = 1
#testPoint3[5] = 1
#testPoint3[6] = 1
#p = clf.predict(testPoint3)
#print("\nPrediction 'working for 6.5 hours':")
#print(p)





