

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


#	index = feature_dict["*&PositiveSum"]
	index = feature_dict[key]
	featureVector[index] = float(numTargetWords)/float(numTotalWords)

	return featureVector


def initDictFromList(list):
	returnDict = {}
	for word in list:
		returnDict[word] = 0
	return returnDict


# this is a function to see how many tweets actually have any temporal comp or counterfactuality
def testDataSet():
	import tweetUtils as tu
	tweets = tu.getTweetsFromFile(8000, "tweets.txt")
	cfList = createListFromFile("../Irony/counterFactuality.txt")
	tcList = createListFromFile("../Irony/temporalCompression.txt")
	numTweetsWithCF = 0
	numTweetsWithTC = 0
	numTotalCF = 0
	numTotalTC = 0

	cfDict = initDictFromList(cfList)
	tcDict = initDictFromList(tcList)

	for tweet in tweets:
		tcFlag = 0
		cfFlag = 0
		tweetAsList = tweet.split()
		for word in tweetAsList:
			if word in cfList:
				numTotalCF += 1
				cfFlag = 1
				cfDict[word] += 1
			elif word in tcList:
				numTotalTC += 1
				tcFlag = 1
				tcDict[word] += 1
		if cfFlag == 1:
			numTweetsWithCF += 1
		elif tcFlag == 1:
			numTweetsWithTC += 1

	print("The total number of temporal compression words in the dataset = " + str(numTotalTC) )
	print("The number of tweets containing a temporal compression word  = " + str(numTweetsWithTC) )
	print("The temporal compression word count dictionary :")
	print(tcDict)
	print("")

	print("The total number of counterfactuality words in the dataset = " + str(numTotalCF) )
	print("The number of tweets containing a counterfactuality word  = " + str(numTweetsWithCF) )
	print("The counterfactuality word count dictionary :")
	print(cfDict)
	print("")





if __name__ == "__main__":
	testDataSet()


