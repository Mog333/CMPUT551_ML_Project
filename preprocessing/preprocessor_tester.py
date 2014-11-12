#! /usr/bin/env python

# This file is a tester for preprecessing methods


FILE_PATH = '../training_data_score_tweet.txt'


def main():
	# get all tweets as a list
	tweet_list = loadData(FILE_PATH)
	#tweet_list = tweet_list[3363:3365]

	"""
	tweet_list = [
		"#tag Alex ups wrt Edmonton pleeeeeeeease",
		"I'm he'll we'll, ;) (; :] :D :p",
		]
	"""

	# this loop precesses tweet by tweets
	for tweet in tweet_list:

		tweet = tweet.lower()

		# normalize words which contain appostrophy
		# as ommission character
		from generalPreprocessingMethods import removeApostrophe
		tweet = removeApostrophe(tweet)


		# remove character repetitions. 
		# Example pleeeeeeeeeeeease => please
		# of the rest part will take care the
		# word corrector
		from generalPreprocessingMethods import removeCharacterRepetitions
		tweet = removeCharacterRepetitions(tweet)

		#print tweet

		# pre-normilize. (imported code) external code, handles some case
		# According to the source of the code:
		# "#Twitter text comes HTML-escaped, so unescape it.
		# We also first unescape &amp;'s, in case the text has been buggily double-escaped."
		from twokenize import normalizeTextForTagger
		tweet = normalizeTextForTagger(tweet)


		# Tokenize! This tokenizer understands emoticons, urls, anotations,
		# hashtags. Repeated the import statement just show where methods
		# come from
		from twokenize import tokenizeRawTweetText
		tweet_tokens = tokenizeRawTweetText(tweet)


		####################################################################
		#	MAPPINGS SECTION

		# map emoticons to positive, negative and neutral (unknown)
		from mappingFunctions import mapEmoticons
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(mapEmoticons(token))

		tweet_tokens = tokens_temp



		"""
		# map locations to a locatio key word
		from mappingFunctions import mapLocations
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(mapLocations(token))

		tweet_tokens = tokens_temp
		"""



		# map brands to a brand key word
		from mappingFunctions import mapBrands
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(mapBrands(token))

		tweet_tokens = tokens_temp



		# slang mapping
		from mappingFunctions import mapSlangs
		tokens_temp = []
		for token in tweet_tokens:

			translated_slang = mapSlangs(token)
			translated_slang = translated_slang.split(' ')
			if (token.strip() == 'youre'):
				print translated_slang
			for i in translated_slang:
				tokens_temp.append(i)


		tweet_tokens = tokens_temp





		# map urls to url key word



		# map images to image key word



		
		# map hashtags
		from mappingFunctions import mapHashtag
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(mapHashtag(token))

		tweet_tokens = tokens_temp




		# map anotations 
		from mappingFunctions import mapAnnotation
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(mapAnnotation(token))

		tweet_tokens = tokens_temp
		


		# map time



		# map date



		# map iterjections





		#	END OF MAPPING SECTION
		####################################################################


		# autmomated spelling mistakes corrector
		from grammarFixer import correct
		tokens_temp = []
		for token in tweet_tokens:
			tokens_temp.append(correct(token))

		tweet_tokens = tokens_temp		



		# Morthing => find a root of the word
		# this alternative to nltk steaming libraries
		# which turned out to work not to well
		from nltk.corpus import wordnet as wn
		tokens_temp = []
		for token in tweet_tokens:
			word = wn.morphy(token)
			if (str(word).strip() != 'None'):
				tokens_temp.append(word)
			else:
				tokens_temp.append(token)


		tweet_tokens = tokens_temp


		# run everything through

		#print tweet_tokens


		# check if if everything is validated
		import enchant
		d = enchant.Dict("en_US")

		for word in tweet_tokens:
			try:
				if(not d.check(str(word).encode('utf-8'))):
					print (word + "\t\t==> invalid")
			except:
				print (word + "\t\t==> invalid")







"""
Reads from file and returns a list of tweets
"""
def loadData(file_path):
	in_file = open(file_path, 'r')

	tweet_list = []
 

	for line in in_file:
		line = line.decode('utf-8')
		tweet_list.append(line.split('\t')[1].replace('\n', ' '))






	in_file.close()
	return tweet_list



main()
