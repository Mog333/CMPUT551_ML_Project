import processTweets as pt 
from sklearn import cross_validation
import numpy as np


def L1Error(prediction, score):
	return abs(prediction - score)


def MeanSquaredError(prediction, score):
	return (prediction - score)**2



def evaluatePrediction(predictions, scores, test_indices, errorFunc):
	totalError = 0
	testScores = scores[test_indices]
	for i in xrange(predictions.shape[0]):
		currentError = errorFunc(predictions[i], testScores[i])
		totalError += currentError

	return totalError/float(predictions.shape[0])



#TODO finsih this (the model has the tweets, or vectors??)
def getPredictionsFromModel(model, test_indices):
	predictions = np.array([])
	for i in test_indices:
		currentPrediction = model[3].predict(model[4][i])
		predictions = np.append(predictions, currentPrediction)
	return predictions



if __name__ == "__main__":
	tweets = pt.getTweetsFromFile("small_tweets2.txt")
	scores = pt.getTweetScoresFromFile("small_score2.txt")
	errorFunc = MeanSquaredError


	kf = cross_validation.KFold(5, n_folds = 2)
	cvErrors = []
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



#pt.main()