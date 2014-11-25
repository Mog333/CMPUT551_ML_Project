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
