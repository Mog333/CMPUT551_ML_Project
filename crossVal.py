import processTweets as pt 
from sklearn import cross_validation
import numpy as np


def L1Error(prediction, score):
	return abs(prediction - score)


def MeanSquaredError(prediction, score):
	return (prediction - score)**2


# given an array of predictions, the actual scores, the indices to test, and
# an error function, returns the average error for the predictions
def evaluatePrediction(predictions, scores, test_indices, errorFunc):
	totalError = 0
	testScores = scores[test_indices]
	for i in xrange(predictions.shape[0]):
		currentError = errorFunc(predictions[i], testScores[i])
		totalError += currentError

	return totalError/float(predictions.shape[0])



# given a trained model and a set of test indices, returns an array containing
# the prediction for each data point at these indices
def getPredictionsFromModel(model, test_indices):
	predictions = np.array([])
	for i in test_indices:
		currentPrediction = model[3].predict(model[4][i])
		predictions = np.append(predictions, currentPrediction)
	return predictions


# given the read-in tweets and scores, the error function to evaluate with,
# the number of folds for cross-validation, and the type of model to use (uni or unibitri)
# this function trains the model and evaluates on the other folds.
# returns a list of each error for the different folds
def crossVal(tweets, scores, errorFunc, numFolds, modelType):
	lenTweets = len(tweets)
	lenScores = len(scores)

	if (lenScores != lenTweets):
		print("The number of tweets does not equal the number of scores!")
		return None

	if (modelType == "uni"):
		modelTrainFunction = pt.trainUnigramModel
	elif (modelType == "uniBiTri"):
		modelTrainFunction = pt.trainUniBiTrigramModel
	else:
		print("Unknown model type!")
		return None

	kf = cross_validation.KFold(lenTweets, n_folds = numFolds) # put in the number of data points and the number of folds
	cvErrors = [] # store the error for each fold
	for train_indices, test_indices in kf:
		#print("TRAIN:", train_indices, "TEST:", test_indices)
		model = modelTrainFunction(train_indices, tweets, scores)
		#print(model[0])
		#print(model[1])
		predictions = getPredictionsFromModel(model, test_indices)
		#print(predictions)
		error = evaluatePrediction(predictions, scores, test_indices, errorFunc)
		cvErrors.append(error)
	return cvErrors



# the main "function". You can import this file and this code won't run
if __name__ == "__main__":
	tweets = pt.getTweetsFromFile("small_tweets2.txt")
	scores = pt.getTweetScoresFromFile("small_score2.txt")
	errorFunc = MeanSquaredError

	cvErrorsUni = crossVal(tweets, scores, errorFunc, 2, "uni")
	print(cvErrorsUni)
	meanErrorOfModel = sum(cvErrorsUni)/float(len(cvErrorsUni))
	print("Error of the uni model = " + str(meanErrorOfModel) )


	cvErrorsBi = crossVal(tweets, scores, errorFunc, 2, "uniBiTri")
	print(cvErrorsBi)
	meanErrorBi = sum(cvErrorsBi)/float(len(cvErrorsBi))
	print("Error of the uniBiTri model = " + str(meanErrorBi) )
	

