

def createDictFromFile(fileName="../SentiWordNet/SentiWordNet.txt"):

	in_file = open(fileName, 'r')

	sentiDict = {}
	for line in in_file:
		wordList = line.split("\t")

		currentWord = wordList[4] # the words in this line
		currentWord = currentWord.split(' ')
		for word in currentWord:
			if word[len(word) -2] == '#':
				newKey = word[:len(word)-2]
				sentiDict[newKey] = (wordList[2], wordList[3]) # the value is a tuple with positive and negative value


	in_file.close()

	return sentiDict



def addSentiToDict(feature_dict):
	feature_dict["*&PositiveSum"] = len(feature_dict)
	feature_dict["*&NegativeSum"] = len(feature_dict)
	return feature_dict



def setFeatureVecForSenti(tweet, featureVector, feature_dict, sentiDict):
	wordsList = tweet.split()
	PositiveSum = 0
	NegativeSum = 0
	for word in wordsList:
		if word in sentiDict:
			try:
				thisPositive = float(sentiDict[word][0])
				thisNegative = float(sentiDict[word][1])
				PositiveSum = PositiveSum + thisPositive
				NegativeSum = NegativeSum + thisNegative
			except ValueError:
				print("Value error: " + word + " " + str(sentiDict[word]))
				continue


	indexPositive = feature_dict["*&PositiveSum"]
	featureVector[indexPositive] = PositiveSum
	indexNegative = feature_dict["*&NegativeSum"] 
	featureVector[indexNegative] = NegativeSum

	return featureVector






