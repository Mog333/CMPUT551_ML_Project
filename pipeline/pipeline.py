import json
import time
from sklearn import cross_validation
import numpy as np

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
	tweets = preprocessTweets.preprocess(tweets, choices)
	t1 = time.time()
	print('Preprocessing done (%.2f s)' % (t1-t0))
else:
	print 'Skip preprocessing'

###
# create and build feature matrix
###
t0 = time.time()
print 'Starting FeatureMatrix creation'
#featureMatrix = createFeatureMatrix(choices)# shape = tweets x features
t1 = time.time()
print('FeatureMatrix created (%.2f s)' % (t1-t0))


###
# pass feature matrix to cross val
###
t0 = time.time()
print 'Starting Crossval'
#result = crossVal(tweets, scores, errorFunc, numFolds, featureMatrix)
t1 = time.time()
print('Crossval done (%.2f s)' % (t1-t0))
print result