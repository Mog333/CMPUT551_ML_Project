import numpy as np

def getTweetsFromFile(count):
   input_file = open('tweets.txt', 'r')
   tweets = np.array([])
   for line in input_file:
      tweets = np.append(tweets, line)
      if(len(tweets) == count):
      	break;
   input_file.close()

   return tweets

def getTweetScoresFromFile(count):
   input_file = open('scores.txt', 'r')
   tweetScores = np.array([])
   for line in input_file:
      score = float(line.lower().replace("\n", ""))
      tweetScores = np.append(tweetScores, score)
      if(len(tweetScores) == count):
      	break;
   input_file.close()
   return np.transpose(tweetScores)