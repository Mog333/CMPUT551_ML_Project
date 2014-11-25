import json
import time
from sklearn import cross_validation
import numpy as np
import pickle
import os

import pipeline_tools
import tweetUtils as pt
from preprocessing import preprocessTweets


choices = pipeline_tools.buildChoiceArray()

print '###'
print '# Project Title'
print '###'
print ''

choices = pipeline_tools.ask(choices)

print ''

print '#####################################'
print 'Starting Calculation with %d examples' % int(choices['num_examples']['value'])
print '#####################################'

tweets = pt.getTweetsFromFile( int(choices['num_examples']['value']) )
scores = pt.getTweetScoresFromFile( int(choices['num_examples']['value']) )

###
# Preprocessing
###
if(choices['preprocessing']['value']):
	t0 = time.time()
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

# handle cache files
cacheFilename = 'fm'
dependencies = ['num_examples']
dependencies += choices['preprocessing']['subs']
dependencies += ['use_unigrams', 'num_unigram_features', 'use_bigrams', 'num_bigram_features']
for param in dependencies:
	cacheFilename += '_' + str(choices[param]['value'])
cacheFilename += '.cache'

if os.path.isfile('cache/' + cacheFilename):
	featureMatrix = pickle.load(open('cache/' + cacheFilename,'rb'))
	print 'Cached featureMatrix file used!'
else:
	import feature
	featureMatrix = feature.createFeatureMatrix(tweets, choices)# shape = tweets x features
	print 'Writing cache file'
	pickle.dump(featureMatrix, open('cache/' + cacheFilename,'wb') )
	print 'Cache file written'

# print type(featureMatrix)
# print len(featureMatrix)
# print len(featureMatrix[0])
# print type(featureMatrix[0][0])
# print featureMatrix.shape()
###
# matrix elements are float.64
###

t1 = time.time()
print('FeatureMatrix created (%.2f s)' % (t1-t0))

print '#####################################'

#print featureMatrix

###
# pass feature matrix to cross val
###
t0 = time.time()
print 'Starting Crossval'
import crossVal
errorFunc = crossVal.MeanSquaredError
result = crossVal.crossVal(tweets, scores, errorFunc, int(choices['cross_num_folds']['value']), featureMatrix)
t1 = time.time()
print('Crossval done (%.2f s)' % (t1-t0))
print result
print '#####################################'
