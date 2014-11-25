#! /usr/bin/env python


import numpy as np
from sklearn import svm
import nltk

#
#  pipeline approach: make functions chainable (processPunct(processEmoticons( . . .)))
#  process functions take string (tweet) - return processed tweet
#  dictionary functions take an existing dictionary, a set of tweets, and parameters and returns the dictionary with new features added
#  feature functions take tweet, its current feature vector, a dictionary, and parameters and returns its modified feature vector 
#

def main():
   train_indices = np.array([0, 1, 2, 3, 4,]) # the indices we use of the data to train. for kfold validation

   # read the tweets and scores from file
   tweets = getTweetsFromFile("small_tweets2.txt")
   scores = getTweetScoresFromFile("small_score2.txt")
   uniModel = trainUnigramModel(train_indices, tweets, scores)
   uniBiTriModel = trainUniBiTrigramModel(train_indices, tweets, scores)
   s1 = "test tweet text"
   s2 = "rob tests tweets"
   s3 = "rob is silly"


   #Unigram model prediction:
   
   uniModelVec1 = np.zeros(len(uniModel[2]))
   uniModelVec2 = np.zeros(len(uniModel[2]))
   uniModelVec3 = np.zeros(len(uniModel[2]))
  
   uniModelVec1 = setFeatureVecForNGram(s1, uniModelVec1, uniModel[2], 1)
   uniModelVec2 = setFeatureVecForNGram(s2, uniModelVec2, uniModel[2], 1)
   uniModelVec3 = setFeatureVecForNGram(s3, uniModelVec3, uniModel[2], 1)

   uniP1 = uniModel[3].predict(uniModelVec1)
   uniP2 = uniModel[3].predict(uniModelVec2)
   uniP3 = uniModel[3].predict(uniModelVec3)

   print("Test Unigram Prediction: \n")
   print("tweet: '" + s1 + "' prediction: " + str(uniP1))
   print("tweet: '" + s2 + "' prediction: " + str(uniP2))
   print("tweet: '" + s3 + "' prediction: " + str(uniP3))

   
   UBT_vec1 = np.zeros(len(uniBiTriModel[2]))
   UBT_vec2 = np.zeros(len(uniBiTriModel[2]))
   UBT_vec3 = np.zeros(len(uniBiTriModel[2]))

   for i in range(1, 4):
      UBT_vec1 = setFeatureVecForNGram(s1, UBT_vec1, uniBiTriModel[2], i)
      UBT_vec2 = setFeatureVecForNGram(s2, UBT_vec2, uniBiTriModel[2], i)
      UBT_vec3 = setFeatureVecForNGram(s3, UBT_vec3, uniBiTriModel[2], i)

   UBT_P1 = uniBiTriModel[3].predict(UBT_vec1)
   UBT_P2 = uniBiTriModel[3].predict(UBT_vec2)
   UBT_P3 = uniBiTriModel[3].predict(UBT_vec3)
   
   print("\nTest Uni/Bi/Trigram prediction: \n")
   print("tweet: '" + s1 + "' prediction: " + str(UBT_P1))
   print("tweet: '" + s2 + "' prediction: " + str(UBT_P2))
   print("tweet: '" + s3 + "' prediction: " + str(UBT_P3))
   
   return (uniModel, uniBiTriModel)
   


def trainUnigramModel(train_indices, tweets, scores):
   #get tweets to train on
   #tweets = tweets[train_indices]
   scores = scores[train_indices]
   
   #build dictionary
   bow_dict = {}
   bow_dict = addNGramToDict(tweets, bow_dict, 1)   
   
   #create empty feature vectors
   featureVectors = createFeatureVectors(tweets, bow_dict)

   #For each feature vector fill it in using dict data
   for i in range(len(tweets)):
      featureVectors[i] = setFeatureVecForNGram(tweets[i], featureVectors[i], bow_dict, 1)

   #append vectors together to make the matrix
   featureMatrix = getFeatureMatrixFromVecs(featureVectors)

   #fit svm model
   clf = svm.SVR()
   clf.fit(featureMatrix[train_indices], scores)
   print("Done fitting")

   #return the tweets, scores, dictionary, and model in a tuple
   return (tweets[train_indices], scores, bow_dict, clf, featureMatrix)   


def trainUniBiTrigramModel(train_indices, tweets, scores):
   #get tweets to train on
   #tweets = tweets[train_indices]
   scores = scores[train_indices]
   
   #build dictionary
   bow_dict = {}
   bow_dict = addNGramToDict(tweets, bow_dict, 1)
   bow_dict = addNGramToDict(tweets, bow_dict, 2)
   bow_dict = addNGramToDict(tweets, bow_dict, 3)   
   
   #create empty feature vectors
   featureVectors = createFeatureVectors(tweets, bow_dict)

   #For each feature vector fill it in using dict data
   for i in range(len(tweets)):
      featureVectors[i] = setFeatureVecForNGram(tweets[i], featureVectors[i], bow_dict, 1)
      featureVectors[i] = setFeatureVecForNGram(tweets[i], featureVectors[i], bow_dict, 2)
      featureVectors[i] = setFeatureVecForNGram(tweets[i], featureVectors[i], bow_dict, 3)

   #append vectors together to make the matrix
   featureMatrix = getFeatureMatrixFromVecs(featureVectors)

   #fit svm model
   clf = svm.SVR()
   clf.fit(featureMatrix[train_indices], scores)
   print("Done fitting")

   #return the tweets, scores, dictionary, and model in a tuple
   return (tweets[train_indices], scores, bow_dict, clf, featureMatrix)   

#
#  Pre processing functions
#  Place in new file when we have several
#  pipeline approach: each process funcion takes a string (tweet), processes it somehow, and returns that tweet
#  processing functions are meant to be chained together
#
def preProcess(words):
   words = words.replace('  ', ' ')
   words = words.replace(',', "")
   words = words.replace('.', '')
   words = words.replace('!', '')
   words = words.replace('\'', '')
   words = words.replace('\"', '')
   words = words.replace('\n', '')
   return words
   

#
#  Unigrams only - First test functions
#  Remove eventually - ngrams / pipeline approach will replace these
#

def buildBOWDictFromTweets(tweetList):
   bow_dict = {}
   number_unique_words = 0
   for tweet in tweetList:
      for word in tweet.split(" "):
         if word in bow_dict:
            bow_dict[word]['count'] += 1
         else:
            bow_dict[word] = {'index':number_unique_words, 'count':1}
            number_unique_words += 1
   return bow_dict

def getFeatureVec(tweet, bow_dict):
   featureVec = np.zeros(len(bow_dict))
   for word in tweet.split(" "):
      try:
         index = bow_dict[word]['index']
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
#
#
#


#
#  N Gram functions
#

def addNGramToDict(tweetList, bow_dict, gramNum):
   #adds n grams to dict, where n is specified (gramNum == 1 => unigrams, gramNum == 2 => bigrams)
   for tweet in tweetList:
      #for each tweet build a list of grams (ie list of words, or bigrams etc)

      gramList= list(nltk.ngrams(tweet.split(), gramNum))
      for gram in gramList:
         if gram in bow_dict:
            bow_dict[gram]['count'] += 1
         else:
            bow_dict[gram] = {'index':len(bow_dict), 'count':1}
   return bow_dict

def setFeatureVecForNGram(tweet, featureVec, bow_dict, n):
   gramList = list(nltk.ngrams(tweet.split(), n))
   for gram in gramList:
      try:
         index = bow_dict[gram]['index']
         featureVec[index] += 1
      except KeyError:
         continue
   
   return featureVec

def createFeatureVectors(tweetList, bow_dict):
   #create empty set of zero vectors to work with one for each tweet
   featureVectors = []
   for t in tweetList:
      featureVectors.append(np.zeros(len(bow_dict)))

   return featureVectors

def getFeatureMatrixFromVecs(vectorList):
   featureMatrix = vectorList[0]
   for vec in vectorList[1:]:
      featureMatrix = np.vstack([featureMatrix, vec])

   return featureMatrix

#
#
#



def getTweetsFromFile(filename):
   input_file = open(filename, 'r')
   tweets = np.array([])
   for line in input_file:
      tweets = np.append(tweets, line.lower())
   input_file.close()

   return tweets

def getTweetScoresFromFile(filename):
   input_file = open(filename, 'r')
   tweetScores = np.array([])
   for line in input_file:
      score = float(line.lower().replace("\n", ""))
      tweetScores = np.append(tweetScores, score)
   input_file.close()
   return np.transpose(tweetScores)




