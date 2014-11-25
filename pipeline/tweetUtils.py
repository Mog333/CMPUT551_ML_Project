import numpy as np

def getTweetsFromFile(count, tweetsFile):
   # input_file = open('tweets.txt', 'r')
   input_file = open(tweetsFile, 'r')
   tweets = []
   for line in input_file:
      tweets.append(line)
      if(len(tweets) == count):
      	break;
   input_file.close()

   return tweets

def getTweetScoresFromFile(count, scoresFile):
   # input_file = open('scores.txt', 'r')
   input_file = open(scoresFile, 'r')
   tweetScores = np.array([])
   for line in input_file:
      score = float(line.lower().replace("\n", ""))
      tweetScores = np.append(tweetScores, score)
      if(len(tweetScores) == count):
      	break;
   input_file.close()
   return np.transpose(tweetScores)
