import gramFeatures

def createFeatureMatrix(tweets, choices):
   bow_dict = {}
   setFunctions = []
   #Create dicitonary with optional features
   if choices['use_unigrams']['value'] == 1:
      numberUnigrams = int(choices['num_unigram_features']['value'])
      bow_dict = gramFeatures.addNGramToDict(tweets, bow_dict, 1, numberUnigrams)
#      setFunctions.append(gramFeatures.setFeatureVecForNGram)

   if choices['use_bigrams']['value'] == 1:
      numberBigrams = int(choices['num_bigram_features']['value'])
      bow_dict = gramFeatures.addNGramToDict(tweets, bow_dict, 2, numberBigrams)
#      setFunctions.append(gramFeatures.setFeatureVecForNGram)


   #Create empty feature vecs
   featureVecs = createFeatureVectors(tweets, bow_dict):
   #Set feature vecs based on choices

   for vec in featureVecs:
      if choices['use_unigrams']['value'] == 1:
         setFeatureVecForNGram(tweets, vec, bow_dict, 1)
      if choices['use_bigrams']['value'] == 1:
         setFeatureVecForNGram(tweets, vec, bow_dict, 2)
   
   matrix = getFeatureMatrixFromVecs(featureVecs)
   return matrix


def createFeatureVectors(tweetList, bow_dict):
   #create empty set of zero vectors to work with one for each tweet
   featureVectors = []
   for t in tweetList:
      featureVectors.append(np.zeros(len(bow_dict)))

   return featureVectors

def getFeatureMatrixFromVecs(vectorList):
   featureMatrix = vectorList[0]
   for vec in vectorList[1:]:
      featureMatrix = np.vstack([featureMatrix, vec])

   return featureMatrix
