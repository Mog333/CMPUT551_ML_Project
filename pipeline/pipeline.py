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
	preprocessCacheFilename = 'ppc'
	
	preprocessCacheFilename += '_' + str(choices['num_examples']['value'])
	for param in choices['preprocessing']['subs']:
		preprocessCacheFilename += '_' + str(choices[param]['value'])
	preprocessCacheFilename += '.cache'

	if os.path.isfile('cache/' + preprocessCacheFilename):
		tweets = pickle.load(open('cache/' + preprocessCacheFilename,'rb'))
		print 'Cached preprocessing file used!'
	else:
		tweets = preprocessTweets.preprocess(tweets, choices)
		pickle.dump(tweets, open('cache/' + preprocessCacheFilename,'wb') )
		print 'Cache file written'
	t1 = time.time()
	print('Preprocessing done (%.2f s)' % (t1-t0))
else:
	print 'Skip preprocessing'


###
# create and build feature matrix
###
t0 = time.time()
print 'Starting FeatureMatrix creation'
import feature
featureMatrix = feature.createFeatureMatrix(tweets, choices)# shape = tweets x features
t1 = time.time()
print('FeatureMatrix created (%.2f s)' % (t1-t0))

# print featureMatrix

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