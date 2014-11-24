#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import processTweets as pt
from nltk.stem.lancaster import LancasterStemmer


def plotScoreHistogram():
   scores = pt.getTweetScoresFromFile("score.txt")
   plt.hist(scores)
   plt.title("Score Histogram")
   plt.xlabel("Value")
   plt.ylabel("Frequency")
   plt.show()

def stemReductionTest():
   st = LancasterStemmer()   
   tweets = pt.getTweetsFromFile("tweet.txt")
   stemCount = 0
   
   bow_dict = {}
   stemmed_dict = {}
   
   for tweet in tweets:
      for word in tweet.split():
         if(word[0] == '@'):
            continue
         
         try:
            stemmedWord = st.stem(word)
         except UnicodeDecodeError:
            stemmedWord = word

         if stemmedWord in stemmed_dict:
            stemmed_dict[stemmedWord]['count'] += 1
         else:
            stemmed_dict[stemmedWord] = {'index':len(stemmed_dict), 'count':1}

   bow_dict = pt.addNGramToDict(tweets, bow_dict, 1)

   print("unigram dict length: " + str(len(bow_dict)) + " stemmed dict length: " + str(len(stemmed_dict)))
   return stemmed_dict
   


def getFreqDict(bow_dict):
   #returns a dictionary with keys being the counts of words in a bow dict, and values being the number of words with that count.
   #ex: freqDict[1] = 15000~ (for our data set) which says there are 15000 words that occur once in the corpus set
   frequencyDict = {}
   for key in bow_dict:
      count = bow_dict[key]['count']
      if count not in frequencyDict:
         frequencyDict[count] = 1
      else:
         frequencyDict[count] += 1
   return frequencyDict


def plotUnigramFrequency():
   tweets = pt.getTweetsFromFile("tweet.txt")
   
   bow_dict = pt.addNGramToDict(tweets, {}, 1)
   
   freqDict = getFreqDict(bow_dict)
   countsList = [freqDict[c] for c in sorted(freqDict.keys())]
   print(freqDict)
   plt.plot(sorted(freqDict.keys()), countsList, 'ro')
   plt.axis([0, max(sorted(freqDict.keys())), 0, max(countsList)])
   plt.show()

   return (tweets, bow_dict, freqDict)


def plotBigramFrequency():
   tweets = pt.getTweetsFromFile("tweet.txt")
   
   bow_dict = pt.addNGramToDict(tweets, {}, 2)
   
   freqDict = getFreqDict(bow_dict)
   countsList = [freqDict[c] for c in sorted(freqDict.keys())]
   print(freqDict)
   plt.plot(sorted(freqDict.keys()), countsList, 'ro')
   plt.axis([0, max(sorted(freqDict.keys())), 0, max(countsList)])
   plt.show()

   return (tweets, bow_dict, freqDict)



