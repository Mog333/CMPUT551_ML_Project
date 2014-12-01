import gramFeatures
import sentimentFeatures as sf
import ironyFeatures as ironyF
import numpy as np
import pipeline_tools

def createFeatureVecFromTweet(tweet, bow_dict, choices):
	
	'''if choices['use_sentiment']['value'] == 1:
		sentiDict = sf.createDictFromFile()
	else:
		sentiDict = {}
		'''
	featureVec = np.zeros(len(bow_dict), dtype=np.float16)

	if choices['use_unigrams']['value'] == 1:
		gramFeatures.setFeatureVecForNGram(tweet, featureVec, bow_dict, 1)
	if choices['use_bigrams']['value'] == 1:
		gramFeatures.setFeatureVecForNGram(tweet, featureVec, bow_dict, 2)
	if choices['use_sentiment']['value'] == 1:
		sentiDict = sf.createDictFromFile()
		sf.setFeatureVecForSenti(tweet, featureVec, bow_dict, sentiDict)
	if choices['use_counterFact']['value'] == 1:
		cfList = ironyF.createListFromFile("../Irony/counterFactuality.txt")
		ironyF.setFeatureVecForRatio(tweets[i], featureMatrix[i], bow_dict, cfList, "*&CounterFactuality")
	if choices['use_temporalComp']['value'] == 1:
		tcList = ironyF.createListFromFile("../Irony/temporalCompression.txt")
		ironyF.setFeatureVecForRatio(tweets[i], featureMatrix[i], bow_dict, tcList, "*&TemporalCompression")

	return featureVec

def createFeatureMatrix(tweets, choices):
	bow_dict = {}

	#Create dicitonary with optional features
	if choices['use_unigrams']['value'] == 1:
#		print("Adding unigrams to dictionary")
		numberUnigrams = int(choices['num_unigram_features']['value'])
		bow_dict = gramFeatures.addNGramToDict(tweets, bow_dict, 1, numberUnigrams)

#	print("Dictionary length unigrams: " + str(len(bow_dict)))

	if choices['use_bigrams']['value'] == 1:
#		print("Adding bigrams to dictionary")
		numberBigrams = int(choices['num_bigram_features']['value'])
		bow_dict = gramFeatures.addNGramToDict(tweets, bow_dict, 2, numberBigrams)

#	print("Dictionary length unigram bigram: " + str(len(bow_dict)))

	if choices['use_sentiment']['value'] == 1:
#		print("Adding sentiment to dictionary")
		sentiDict = sf.createDictFromFile()
		bow_dict = sf.addSentiToDict(bow_dict)
#		print("Dictionary length sentiment: " + str(len(bow_dict)))
	else:
		sentiDict = {}

	if choices['use_counterFact']['value'] == 1:
#		print("Adding counterFactuality to dictionary")
		cfList = ironyF.createListFromFile("../Irony/counterFactuality.txt")
		bow_dict = ironyF.addCounterFactToDict(bow_dict)
#		print("Dictionary length counterFactuality: " + str(len(bow_dict)))
	else:
		cfList = []

	if choices['use_temporalComp']['value'] == 1:
#		print("Adding temporalCompression to dictionary")
		tcList = ironyF.createListFromFile("../Irony/temporalCompression.txt")
		bow_dict = ironyF.addTemporalCompToDict(bow_dict)
#		print("Dictionary length temporalCompression: " + str(len(bow_dict)))
	else:
		tcList = []

#	print("Matrix creation")
	featureMatrix = np.zeros((len(tweets), len(bow_dict)), dtype=np.float16)

	for i in range(0, len(tweets)):
		percent = 1.0 * i / len(tweets)
		pipeline_tools.statusbar(percent, 'Setting Feature Vectors')
		if choices['use_unigrams']['value'] == 1:
			gramFeatures.setFeatureVecForNGram(tweets[i], featureMatrix[i], bow_dict, 1)
		if choices['use_bigrams']['value'] == 1:
			gramFeatures.setFeatureVecForNGram(tweets[i], featureMatrix[i], bow_dict, 2)
		if choices['use_sentiment']['value'] == 1:
			sf.setFeatureVecForSenti(tweets[i], featureMatrix[i], bow_dict, sentiDict)
		if choices['use_counterFact']['value'] == 1:
			ironyF.setFeatureVecForRatio(tweets[i], featureMatrix[i], bow_dict, cfList, "*&CounterFactuality")
		if choices['use_temporalComp']['value'] == 1:
			ironyF.setFeatureVecForRatio(tweets[i], featureMatrix[i], bow_dict, tcList, "*&TemporalCompression")
	pipeline_tools.statusbar(1, 'Setting Feature Vectors')


	return {'featureMatrix':featureMatrix, "dict":bow_dict}
