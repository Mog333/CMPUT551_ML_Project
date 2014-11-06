#! /usr/bin/env python


import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import processTweets as pt

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

   return freqDict
