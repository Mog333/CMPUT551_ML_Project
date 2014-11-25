import json
import time
from sklearn import cross_validation
import numpy as np

import pipeline_tools
import processTweets as pt
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
# errorFunc = MeanSquaredError

if(choices['preprocessing']['value']):

	# preprocessCacheFilename = 'ppc'
	# preprocessCacheFilename += '_' + str(choices[0]['value'])
	# for tmp in choices[1]['subs']:
	# 	preprocessCacheFilename += '_' + str(tmp['value'])
	# print preprocessCacheFilename

	t0 = time.time()
	print 'Starting preprocessing'
	tweets = preprocessTweets.preprocess(tweets, choices)
	t1 = time.time()
	print('Preprocessing done (%.2f s)' % (t1-t0))
	# np.save(outfile, tweets)
else:
	print 'Skip preprocessing'

# build dict
# create feature vetcs ## all 0
# build feature vects ## bow count
# create feature matrix from vects
# pass feature matrix to cross val

# print json.dumps(choices)