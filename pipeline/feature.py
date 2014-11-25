import gramFeatures
import sentimentFeatures as sf
import numpy as np
import pipeline_tools

def createFeatureMatrix(tweets, choices):
	bow_dict = {}

	
	#Create dicitonary with optional features
	if choices['use_unigrams']['value'] == 1:
		print("Adding unigrams to dictionary")
		numberUnigrams = int(choices['num_unigram_features']['value'])
		bow_dict = gramFeatures.addNGramToDict(tweets, bow_dict, 1, numberUnigrams)

	print("Dictionary length unigrams: " + str(len(bow_dict)))

	if choices['use_bigrams']['value'] == 1:
		print("Adding bigrams to dictionary")
		numberBigrams = int(choices['num_bigram_features']['value'])
		bow_dict = gramFeatures.addNGramToDict(tweets, bow_dict, 2, numberBigrams)

	print("Dictionary length unigram bigram: " + str(len(bow_dict)))

	if choices['use_sentiment']['value'] == 1:
		print("Adding sentiment to dictionary")
		sentiDict = sf.createDictFromFile()
		bow_dict = sf.addSentiToDict(bow_dict)
		print("Dictionary length sentiment: " + str(len(bow_dict)))
	else:
		sentiDict = {}
	print("Matrix creation")
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
	pipeline_tools.statusbar(1, 'Setting Feature Vectors')


	return {'featureMatrix':featureMatrix, "dict":bow_dict}
