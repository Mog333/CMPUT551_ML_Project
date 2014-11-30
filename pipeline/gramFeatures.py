import numpy as np
from sklearn import svm
import nltk


def addNGramToDict(tweetList, bow_dict, gramNum = 1, numFeatures = -1):
   #keep numFeatures in the dict, or remove total_features_created - numFeatures
   #if numFeatures is a fraction, .9 or 90% keep 90%. ie remove total_features_created - numFeatures * total_features_created
   #adds n grams to dict, where n is specified (gramNum == 1 => unigrams, gramNum == 2 => bigrams)

   newFeaturesDict = {}
   for tweet in tweetList:
      #for each tweet build a list of grams (ie list of words, or bigrams etc)
      gramList= list(nltk.ngrams(tweet.split(), gramNum))
      for gram in gramList:
         if gramNum != 1 and (gram[0][0:2] == '*&' or gram[0][0:3] == '*@&'):
            #skip all non unigrams with special tokens
            continue
         if gram in newFeaturesDict:
            newFeaturesDict[gram] += 1
         else:
            newFeaturesDict[gram] = 1

   #analyse numFeatures to determine number of features to add
   #negative means add all
   # < 1 means add that percent (.7 = add 70% most common grams)
   # >= 1 means add that many features (add numFeatures = 100 => add 100 most common features)

   numAdded = 0
   if numFeatures < 0:
      numFeatures = len(newFeaturesDict) + 1
   if numFeatures < 1:
      numFeatures = len(newFeaturesDict) * numFeatures
   defaultLen= len(bow_dict)

   #add numFeatures to the already existing dictionary, assigning new indicies as you go

   for item in sorted(newFeaturesDict.items(), key =lambda tup: tup[1], reverse=True):
      bow_dict[item[0]] = {'index': defaultLen + numAdded, 'count':item[1]}
      numAdded += 1
      if numAdded >= numFeatures:
         break;

   return bow_dict


#Frequency features - not presence
def setFeatureVecForNGram(tweet, featureVec, bow_dict, n):
   # type(tweet)
   gramList = list(nltk.ngrams(tweet.split(), n))
   for gram in gramList:
      try:
         index = bow_dict[gram]['index']
         featureVec[index] += 1
      except KeyError:#unknown feature found
         continue

   return featureVec

