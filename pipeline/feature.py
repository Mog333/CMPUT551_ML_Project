import gramFeatures
import numpy as np
import pipeline_tools

def createFeatureMatrix(tweets, choices):
	bow_dict = {}

	
	#Create dicitonary with optional features
	if choices['use_unigrams']['value'] == 1:
		print("Adding unigrams to dictionary")
		numberUnigrams = int(choices['num_unigram_features']['value'])
		bow_dict = gramFeatures.addNGramToDict(tweets, bow_dict, 1, numberUnigrams)


	if choices['use_bigrams']['value'] == 1:
		print("Adding bigrams to dictionary")
		numberBigrams = int(choices['num_bigram_features']['value'])
		bow_dict = gramFeatures.addNGramToDict(tweets, bow_dict, 2, numberBigrams)

	print("Dictionary length: " + str(len(bow_dict)))

	print("Matrix creation")
	featureMatrix = np.zeros((len(tweets), len(bow_dict)), dtype=np.float16)

	for i in range(0, len(tweets)):
		percent = 1.0 * i / len(tweets)
		pipeline_tools.statusbar(percent, 'Setting Feature Vectors')
		if choices['use_unigrams']['value'] == 1:
			gramFeatures.setFeatureVecForNGram(tweets[i], featureMatrix[i], bow_dict, 1)
		if choices['use_bigrams']['value'] == 1:
			gramFeatures.setFeatureVecForNGram(tweets[i], featureMatrix[i], bow_dict, 2)
	pipeline_tools.statusbar(1, 'Setting Feature Vectors')

	return featureMatrix
