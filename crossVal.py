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



# the main "function". You can import this file and this code won't run
if __name__ == "__main__":
	tweets = pt.getTweetsFromFile("small_tweets2.txt")
	scores = pt.getTweetScoresFromFile("small_score2.txt")
	errorFunc = MeanSquaredError


	kf = cross_validation.KFold(5, n_folds = 2) # put in the number of data points and the number of folds
	cvErrors = [] # store the error for each fold
	for train_indices, test_indices in kf:
		print("TRAIN:", train_indices, "TEST:", test_indices)
		uniModel = pt.trainUnigramModel(train_indices, tweets, scores)
		#print(uniModel[4])
		predictions = getPredictionsFromModel(uniModel, test_indices)
		error = evaluatePrediction(predictions, scores, test_indices, errorFunc)
		cvErrors.append(error)

	meanErrorOfModel = sum(cvErrors)/float(len(cvErrors))
	print("Error of the model = " + str(meanErrorOfModel) )
	print(cvErrors)

