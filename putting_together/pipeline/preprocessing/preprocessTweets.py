import pipeline_tools

def preprocess(tweet_list, choices):
	# print choices
	for key,tweet in enumerate(tweet_list):
		percent = 1.0 * key / len(tweet_list)
		pipeline_tools.statusbar(percent, 'Preprocessing')

		# lower case
		if(choices[0]['value'] == 1):
			tweet = tweet.lower()

		# normalize words which contain appostrophy
		# as ommission character
		if(choices[1]['value'] == 1):
			from generalPreprocessingMethods import removeApostrophe
			tweet = removeApostrophe(tweet)

		# remove character repetitions. 
		# Example pleeeeeeeeeeeease => please
		# of the rest part will take care the
		# word corrector
		if(choices[2]['value'] == 1):
			from generalPreprocessingMethods import removeCharacterRepetitions
			tweet = removeCharacterRepetitions(tweet)

		# pre-normilize. (imported code) external code, handles some case
		# According to the source of the code:
		# "#Twitter text comes HTML-escaped, so unescape it.
		# We also first unescape &amp;'s, in case the text has been buggily double-escaped."
		if(choices[3]['value'] == 1):
			from twokenize import normalizeTextForTagger
			tweet = normalizeTextForTagger(tweet)

	pipeline_tools.statusbar(1, 'Preprocessing')
	return tweet_list