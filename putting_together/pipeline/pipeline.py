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
print 'Starting Calculation with %d examples' % int(choices[0]['pos_values'][ choices[0]['value'] ])
print '#####################################'

tweets = pt.getTweetsFromFile( int(choices[0]['pos_values'][ choices[0]['value'] ]) )
scores = pt.getTweetScoresFromFile( int(choices[0]['pos_values'][ choices[0]['value'] ]) )
# errorFunc = MeanSquaredError

if(choices[1]['value']):

	preprocessCacheFilename = 'ppc'
	preprocessCacheFilename += '_' + str(choices[0]['value'])
	for tmp in choices[1]['subs']:
		preprocessCacheFilename += '_' + str(tmp['value'])
	print preprocessCacheFilename

	t0 = time.time()
	print 'Starting preprocessing'
	tweets = preprocessTweets.preprocess(tweets, choices[1]['subs'])
	t1 = time.time()
	print('Preprocessing done (%.2f s)' % (t1-t0))
	# np.save(outfile, tweets)
else:
	print 'Skip preprocessing'


# print json.dumps(choices)