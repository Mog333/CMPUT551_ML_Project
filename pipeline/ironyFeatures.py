

def createListFromFile(fileName):

	in_file = open(fileName, 'r')

	wordList = []
	for line in in_file:
		words = line.split() # do this to remove newline char if there
		wordList.append(words[0])
	in_file.close()

	return wordList



def addCounterFactToDict(feature_dict):
	feature_dict["*&CounterFactuality"] = len(feature_dict)
	return feature_dict

def addTemporalCompToDict(feature_dict):
	feature_dict["*&TemporalCompression"] = len(feature_dict)
	return feature_dict


#key is a string that is an index into the feature_dict(ex. "*&TemporalCompression")
def setFeatureVecForRatio(tweet, featureVector, feature_dict, wordList, key):
	tweetAsList = tweet.split()
	numTargetWords = 0
	numTotalWords= 0
	for word in tweetAsList:
		numTotalWords += 1
		if word in wordList:
			numTargetWords +=1


	index = feature_dict["*&PositiveSum"]
	featureVector[index] = float(numTargetWords)/float(numTotalWords)

	return featureVector






