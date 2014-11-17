import processTweets as pt 
import time
from sklearn import cross_validation
import numpy as np
import sys

def preprocess(tweet_list):

	# this loop precesses tweet by tweets
	for key,tweet in enumerate(tweet_list):
		percent = 1.0 * key / len(tweet_list)
		statusbar(percent, 'Preprocessing')

		tweet = tweet.lower()

		# normalize words which contain appostrophy
		# as ommission character
		from generalPreprocessingMethods import removeApostrophe
		tweet = removeApostrophe(tweet)


		# remove character repetitions. 
		# Example pleeeeeeeeeeeease => please
		# of the rest part will take care the
		# word corrector
		from generalPreprocessingMethods import removeCharacterRepetitions
		tweet = removeCharacterRepetitions(tweet)

		# pre-normilize. (imported code) external code, handles some case
		# According to the source of the code:
		# "#Twitter text comes HTML-escaped, so unescape it.
		# We also first unescape &amp;'s, in case the text has been buggily double-escaped."
		from twokenize import normalizeTextForTagger
		tweet = normalizeTextForTagger(tweet)


		# Tokenize! This tokenizer understands emoticons, urls, anotations,
		# hashtags. Repeated the import statement just show where methods
		# come from
		from twokenize import tokenizeRawTweetText
		tweet_tokens = tokenizeRawTweetText(tweet)

		####################################################################
		#	MAPPINGS SECTION

		# map emoticons to positive, negative and neutral (unknown)
		from mappingFunctions import mapEmoticons
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(mapEmoticons(token))

		tweet_tokens = tokens_temp

		# map brands to a brand key word
		from mappingFunctions import mapBrands
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(mapBrands(token))

		tweet_tokens = tokens_temp



		# slang mapping
		from mappingFunctions import mapSlangs
		tokens_temp = []
		for token in tweet_tokens:

			translated_slang = mapSlangs(token)
			translated_slang = translated_slang.split(' ')
			# if (token.strip() == 'youre'):
			# 	print translated_slang
			for i in translated_slang:
				tokens_temp.append(i)


		tweet_tokens = tokens_temp

		# map urls to url key word



		# map images to image key word



		
		# map hashtags
		from mappingFunctions import mapHashtag
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(mapHashtag(token))

		tweet_tokens = tokens_temp




		# map anotations 
		from mappingFunctions import mapAnnotation
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(mapAnnotation(token))

		tweet_tokens = tokens_temp
		


		# map time



		# map date



		# map iterjections





		#	END OF MAPPING SECTION
		####################################################################


		# autmomated spelling mistakes corrector
		from grammarFixer import correct
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(correct(token))

		tweet_tokens = tokens_temp		



		# Morthing => find a root of the word
		# this alternative to nltk steaming libraries
		# which turned out to work not to well
		# from nltk.corpus import wordnet as wn
		# tokens_temp = []
		# for token in tweet_tokens:
		# 	word = wn.morphy(token)
		# 	if (str(word).strip() != 'None'):
		# 		tokens_temp.append(word)
		# 	else:
		# 		tokens_temp.append(token)


		# tweet_tokens = tokens_temp


		# run everything through

		#print tweet_tokens


		# check if if everything is validated
		# import enchant
		# d = enchant.Dict("en_US")

		# for word in tweet_tokens:
		# 	try:
		# 		if(not d.check(str(word).encode('utf-8'))):
		# 			print (word + "\t\t==> invalid")
		# 	except:
		# 		print (word + "\t\t==> invalid")

		tweet_list[key] = tweet
	statusbar(1, 'Preprocessing')

	return tweet_list

def MeanSquaredError(prediction, score):
	return (prediction - score)**2

# given a trained model and a set of test indices, returns an array containing
# the prediction for each data point at these indices
def getPredictionsFromModel(model, test_indices):
	predictions = np.array([])
	for i in test_indices:
		currentPrediction = model[3].predict(model[4][i])
		predictions = np.append(predictions, currentPrediction)
	return predictions

# given an array of predictions, the actual scores, the indices to test, and
# an error function, returns the average error for the predictions
def evaluatePrediction(predictions, scores, test_indices, errorFunc):
	totalError = 0
	testScores = scores[test_indices]
	for i in xrange(predictions.shape[0]):
		currentError = errorFunc(predictions[i], testScores[i])
		totalError += currentError

	return totalError/float(predictions.shape[0])

def statusbar(percent, text):
   sys.stdout.write("\r")
   progress = ""
   for i in range(20):
      if i < int(20 * percent):
         progress += "="
      else:
         progress += " "
   sys.stdout.write("%s: [ %s ] %.2f%%" % (text, progress, percent * 100))
   sys.stdout.flush()

   if(percent == 1):
      print ''

def statusbar2(percent):
	progress = ""
	for i in range(20):
		if i < int(20 * percent):
			progress += "="
		else:
			progress += " "

	readFile = open("output.txt")
	lines = readFile.readlines()
	readFile.close()
	w = open("output.txt",'w')
	if(percent != 0):
		w.writelines([item for item in lines[:-1]])
	else:
		w.writelines([item for item in lines])
	w.write("[ %s ] %.2f%%\n" % (progress, percent * 100))
	w.close()

tweets = pt.getTweetsFromFile('tweets.txt')
scores = pt.getTweetScoresFromFile("scores.txt")
errorFunc = MeanSquaredError

print '#####################################'
print 'Starting Calculation with %d examples' % len(tweets)
print '#####################################'

t0 = time.time()
print 'Starting preprocessing'
tweets = preprocess(tweets)
t1 = time.time()
print('Preprocessing done (%.2f s)' % (t1-t0))

t0 = time.time()
print 'Starting cross validation'

kf = cross_validation.KFold(5, n_folds = 2) # put in the number of data points and the number of folds
cvErrors = [] # store the error for each fold
for train_indices, test_indices in kf:
 	print("TRAIN:", train_indices, "TEST:", test_indices)
 	uniModel = pt.trainUnigramModel(train_indices, tweets, scores)
# 	print(uniModel[4])
 	predictions = getPredictionsFromModel(uniModel, test_indices)
 	error = evaluatePrediction(predictions, scores, test_indices, errorFunc)
 	cvErrors.append(error)

meanErrorOfModel = sum(cvErrors)/float(len(cvErrors))
print("Error of the model = " + str(meanErrorOfModel) )
print(cvErrors)

t1 = time.time()
print('Cross validation done (%.2f s)' % (t1-t0))