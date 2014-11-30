#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import gramFeatures
import tweetUtils as pt
import pipeline_tools
import pipeline
import os
import pickle

import sys
from nltk.stem.lancaster import LancasterStemmer
from preprocessing import preprocessTweets

def findBaseLineError():
	scores = pt.getTweetScoresFromFile(-1, "scores.txt")
	total = 0
	
	for score in scores:
		total += score
	
	mean = total / len(scores)
	print("mean: " + str(mean))
	MSE = 0
	ADE = 0
	
	for score in scores:
		ADE += abs(score - mean)		
		MSE += (score - mean)**2
	MSE /= len(scores)
	ADE /= len(scores)
	print("MSE: "+str(MSE))
	print("ADE: " + str(ADE))

def plotScoreHistogram():
	scores = pt.getTweetScoresFromFile(-1, "scores.txt")
	plt.hist(scores)
	plt.title("Score Histogram")
	plt.xlabel("Value")
	plt.ylabel("Frequency")
	plt.show()



def preProcess(tweets, ini_filename):
	choices = pipeline_tools.buildChoiceArray()
	choices = pipeline_tools.ask(choices, ini_filename = ini_filename)

	if(choices['preprocessing']['value']):
		print 'Starting preprocessing'

		# handle cache files
		cacheFilename = 'ppc'
		dependencies = ['num_examples']
		dependencies += choices['preprocessing']['subs']
		for param in dependencies:
			cacheFilename += '_' + str(choices[param]['value'])
		cacheFilename += '.cache'

		if os.path.isfile('cache/' + cacheFilename):
			tweets = pickle.load(open('cache/' + cacheFilename,'rb'))
			print 'Cached preprocessing file used!'
		else:
			tweets = preprocessTweets.preprocess(tweets, choices)
			pickle.dump(tweets, open('cache/' + cacheFilename,'wb') )
			print 'Cache file written'

		print('Preprocessing done')
	else:
		print 'Skip preprocessing'
	return tweets



def stemReductionTest():
	st = LancasterStemmer()	
	tweets = pt.getTweetsFromFile(-1, "tweets.txt")
	tweets = preProcess(tweets, 'allGrams.ini')	
	
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

	bow_dict = gramFeatures.addNGramToDict(tweets, bow_dict, 1, -1)

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
	tweets = pt.getTweetsFromFile(-1, "tweets.txt")
	tweets = preProcess(tweets, 'allGrams.ini')	

	bow_dict = gramFeatures.addNGramToDict(tweets, {}, 1, -1)
	
	freqDict = getFreqDict(bow_dict)
	countsList = [freqDict[c] for c in sorted(freqDict.keys())]
	print(freqDict)
	plt.plot(sorted(freqDict.keys()), countsList, 'ro')
	plt.axis([0, max(sorted(freqDict.keys())), 0, max(countsList)])
	plt.show()

	return (tweets, bow_dict, freqDict)


def plotBigramFrequency():
	tweets = pt.getTweetsFromFile(-1, "tweets.txt")
	tweets = preProcess(tweets, 'allGrams.ini')
	
	bow_dict = gramFeatures.addNGramToDict(tweets, {}, 2, -1)
	
	freqDict = getFreqDict(bow_dict)
	countsList = [freqDict[c] for c in sorted(freqDict.keys())]
	print(freqDict)
	plt.plot(sorted(freqDict.keys()), countsList, 'ro')
	plt.axis([0, max(sorted(freqDict.keys())), 0, max(countsList)])
	plt.show()

	return (tweets, bow_dict, freqDict)



