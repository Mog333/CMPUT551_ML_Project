import json
import time
import sys
import os
import sklearn
from sklearn import cross_validation
from sklearn import svm
import numpy as np
import pickle
import os
import feature
import pipeline_tools
import tweetUtils as pt
import crossVal
from preprocessing import preprocessTweets

def test(fold = 50):
	mo = trainModelForTesting('init2.ini')
	tweets = pt.getTweetsFromFile( int(mo['choices']['num_examples']['value']) , 'tweets.txt')
	scores = pt.getTweetScoresFromFile( int(mo['choices']['num_examples']['value']) , 'scores.txt')
	prediction1 = []	
	prediction2 = []
	for i in range(fold):
		#prediction1.append(predictUsingModel(mo, tweets[i])['prediction'])
		prediction2.append(mo['model'].predict(mo['featureObject']['featureMatrix'][i]))

	for i in range(fold):
		print(str(i+1) + ":" + str(prediction2[i]))
		
	
def predictUsingModel(modelObject, tweet):
	if(modelObject['choices']['preprocessing']['value']):
		print 'Starting preprocessing'
		tweets = [tweet]
		tweets = preprocessTweets.preprocess(tweets, modelObject['choices'])
		tweet = tweets[0]
	else:
		print 'Skip preprocessing'

	featureVec = feature.createFeatureVecFromTweet(tweet, modelObject['featureObject']['dict'], modelObject['choices'])
	return {'prediction':modelObject['model'].predict(featureVec), 'tweet': tweet}

def trainModelForTesting(filename = '', tweetsFile = 'tweets.txt', scoresFile = 'scores.txt'):
	choices = pipeline_tools.buildChoiceArray()
	choices = pipeline_tools.ask(choices, ini_filename = filename)

	tweets = pt.getTweetsFromFile( int(choices['num_examples']['value'] + 50) , tweetsFile)
	scores = pt.getTweetScoresFromFile( int(choices['num_examples']['value'] + 50) , scoresFile)

	if(choices['preprocessing']['value']):
		t0 = time.time()
		print 'Starting preprocessing'

		# handle cache files
		cacheFilename = 'ppc' + tweetsFile + "_"
		dependencies = ['num_examples']
		dependencies += choices['preprocessing']['subs']
		for param in dependencies:
			cacheFilename += '_' + str(choices[param]['value'])
		cacheFilename += '.cache'

		if os.path.isfile('cache/' + cacheFilename):
			tweets = pickle.load(open('cache/' + cacheFilename,'rb'))
			tweets = tweets[50:]
			scores = scores[50:]

			print 'Cached preprocessing file used!'
		else:
			tweets = tweets[50:]
			scores = scores[50:]
			tweets = preprocessTweets.preprocess(tweets, choices)
			pickle.dump(tweets, open('cache/' + cacheFilename,'wb') )
			print 'Cache file written'
		t1 = time.time()
		print('Preprocessing done (%.2f s)' % (t1-t0))
	else:
		print 'Skip preprocessing'

	t0 = time.time()
	print 'Creating Feature Matrix'
	featureObject = feature.createFeatureMatrix(tweets, choices)
	featureMatrix = featureObject['featureMatrix']
	t1 = time.time()
	print('FeatureMatrix created (%.2f s)' % (t1-t0))

	modelDict = {0: 'linear', 1: 'rbf', 2:'poly'}
	modelType = modelDict[choices['svm_model']['value']]
	modelDegree = choices['svm_degree']['value']

	t0 = time.time()
	clf = svm.SVR(modelType, degree = modelDegree)
	clf.fit(featureMatrix, scores)
	t1 = time.time()
	print('Model trained (%.2f s)' % (t1-t0))
	
	return {'model':clf, "featureObject":featureObject, 'choices':choices}

	

def main(filename = '', tweetsFile = 'tweets.txt', scoresFile = 'scores.txt'):
	choices = pipeline_tools.buildChoiceArray()

	print '###'
	print '# Project Title'
	print '###'
	print ''
	
	choices = pipeline_tools.ask(choices, ini_filename = filename)

	print ''

	print '#####################################'
	print 'Starting Calculation with %d examples' % int(choices['num_examples']['value'])
	print '#####################################'

	tweets = pt.getTweetsFromFile( int(choices['num_examples']['value']) , tweetsFile)
	scores = pt.getTweetScoresFromFile( int(choices['num_examples']['value']) , scoresFile)

	###
	# Preprocessing
	###
	if(choices['preprocessing']['value']):
		t0 = time.time()
		print 'Starting preprocessing'

		# handle cache files
		cacheFilename = 'ppc_' + tweetsFile[0:-4] + "_"
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
		t1 = time.time()
		print('Preprocessing done (%.2f s)' % (t1-t0))
	else:
		print 'Skip preprocessing'

	print '#####################################'


	###
	# create and build feature matrix
	###
	t0 = time.time()
	print 'Starting FeatureMatrix creation'

	#caching takes longer than rebuilding

	# handle cache files
#	cacheFilename = 'fm'
#	dependencies = ['num_examples']
#	dependencies += choices['preprocessing']['subs']
#	dependencies += ['use_unigrams', 'num_unigram_features', 'use_bigrams', 'num_bigram_features']
#	for param in dependencies:
#		cacheFilename += '_' + str(choices[param]['value'])
#	cacheFilename += '.cache'

	#if os.path.isfile('cache/' + cacheFilename):
	#	featureMatrix = pickle.load(open('cache/' + cacheFilename,'rb'))
	#	print 'Cached featureMatrix file used!'
	#else:
	#	
	#	featureMatrix = feature.createFeatureMatrix(tweets, choices)# shape = tweets x features
	#	print 'Writing cache file'
	#	pickle.dump(featureMatrix, open('cache/' + cacheFilename,'wb') )
	#	print 'Cache file written'
	featureObject = feature.createFeatureMatrix(tweets, choices)
	featureMatrix = featureObject['featureMatrix']	
#	print(featureMatrix)

	t1 = time.time()
	print('FeatureMatrix created (%.2f s)' % (t1-t0))

	print '#####################################'

	#print featureMatrix

	###
	# pass feature matrix to cross val
	###
	t0 = time.time()
	print 'Starting Crossval'
	
	errorFunc = crossVal.MeanSquaredError
		
	result = crossVal.crossVal(tweets, scores, errorFunc, choices, featureMatrix)
	t1 = time.time()
	print('Crossval done (%.2f s)' % (t1-t0))
	print result
	print '#####################################'

	featureObject['choices'] = choices
	return featureObject

###
#	Accept a list of ini files, run pipeline on all files and log crossval errors in modeloutput.txt
###
def runModelsAndLog(ini_files, outputFilename = 'modelOutput.txt', tweetsFile = 'tweets.txt', scoresFile = 'scores.txt'):
	loadedTweets = pt.getTweetsFromFile( -1 , tweetsFile)
	loadedScores = pt.getTweetScoresFromFile( -1, scoresFile)
	outputFile = open(outputFilename, 'w')

	crossval_errors = []
	for ini_file in ini_files:
		outputFile.write("Choices File: " + ini_file + "\n")
		choices = pipeline_tools.buildChoiceArray()
		choices = pipeline_tools.ask(choices, ini_filename = ini_file)
		tweets = loadedTweets[0:int(choices['num_examples']['value'])]
		scores = loadedScores[0:int(choices['num_examples']['value'])]

		if(choices['preprocessing']['value']):
			t0 = time.time()

			# handle cache files
			cacheFilename = 'ppc_' + tweetsFile[0:-4] + "_"
			dependencies = ['num_examples']
			dependencies += choices['preprocessing']['subs']
			for param in dependencies:
				cacheFilename += '_' + str(choices[param]['value'])
			cacheFilename += '.cache'

			if os.path.isfile('cache/' + cacheFilename):
				tweets = pickle.load(open('cache/' + cacheFilename,'rb'))
			else:
				tweets = preprocessTweets.preprocess(tweets, choices)
				pickle.dump(tweets, open('cache/' + cacheFilename,'wb') )
			t1 = time.time()
			outputFile.write("\t" + 'Preprocessing done (%.2f s)\n' % (t1-t0))

		t0 = time.time()
		featureObject = feature.createFeatureMatrix(tweets, choices)
		featureMatrix = featureObject['featureMatrix']	
		t1 = time.time()
		outputFile.write("\t" + 'FeatureMatrix created (%.2f s)\n' % (t1-t0))

		t0 = time.time()
		errorFunc = crossVal.MeanSquaredError
		result = crossVal.crossVal(tweets, scores, errorFunc, choices, featureMatrix)
		t1 = time.time()
		outputFile.write("\t" + 'Crossval time (%.2f s)\n' % (t1-t0))
		outputFile.write("\t" + "Results: " + str(result) + "\n")

	outputFile.close()

if __name__ == "__main__":
	filename = ''
	if(len(sys.argv) >= 2):
		filename = sys.argv[1]
	main(filename)
