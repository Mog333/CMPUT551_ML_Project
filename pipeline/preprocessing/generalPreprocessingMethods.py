#! /usr/bin/env python

# This file file contains general preprocessing methods


# there are no (or not many) English words  which contain 
# repetitions of a character more than twice. So this method 
# removes character duplicas till no repetitions. Further 
# the automatical grammar corector must resolve the problem 
def removeCharacterRepetitions(tweet):
	# traverse by 3 characters at a time
	# if same => remove two character
	
	# remove all duplicates 
	#import itertools
	#return ''.join(ch for ch, _ in itertools.groupby(tweet))

	if len(tweet) <= 2:
		return tweet
	else:
		new_tweet = tweet[0: 2]

		for ch in range(2, len(tweet)):
			if (not(tweet[ch] == tweet[ch - 1] and 
				tweet[ch - 1] == tweet[ch - 2])):
					new_tweet += tweet[ch]
		return new_tweet

		

#Remove tweet names like @robpost
def removeTwitterNames(tweet):
	wordList = tweet.split()
	newTweet = ""
	for word in wordList:
		if word[0] != '@':
			newTweet += word + " "
	return newTweet

# This method remover appostrophis in cases when it 
# is used as character ommision
def removeApostrophe(tweet):
	tweet = tweet.replace('it\'s ', ' it is ')
	tweet = tweet.replace('won\'t ', ' would not ')
	tweet = tweet.replace('can\'t ', ' can not ')
	tweet = tweet.replace('does\'t ', ' does not ')
	tweet = tweet.replace('n\'t ', ' not ')
	tweet = tweet.replace('\'m ', ' am ')
	tweet = tweet.replace('\'ll ', ' will ')
	tweet = tweet.replace('\'ve ', ' have ')
	tweet = tweet.replace('\'re ', ' are ')

	return tweet







