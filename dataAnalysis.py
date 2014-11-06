#! /usr/bin/env python


import numpy as np
from sklearn import svm

def getFreqDict(bow_dict):
   #returns a dictionary with keys being the counts of words in a bow dict, and values being the number of words with that count.
   #ex: freqDict[1] = 15000~ (for our data set) which says there are 15000 words that occur once in the corpus set
   frequencyDict = {}
   for key in d:
      c = d[key]['count']
      if c not in frequencyDict:
         frequencyDict[c] = 1
      else:
         frequencyDict[c] += 1
   return frequencyDict

