import pipeline_tools

def preprocess(tweet_list, choices):
	for key,tweet in enumerate(tweet_list):
		#print ('\n' + tweet)
		percent = 1.0 * key / len(tweet_list)
		pipeline_tools.statusbar(percent, 'Preprocessing')

		# remove non-ascii characters
		tweet = ''.join([i if ord(i) < 128 else ' ' for i in tweet])

		# lower case
		if(choices['pre_lower_chars']['value'] == 1):
			tweet = tweet.lower()

		# normalize words which contain appostrophy
		# as ommission character
		if(choices['pre_appostrophy']['value'] == 1):
			from generalPreprocessingMethods import removeApostrophe
			tweet = removeApostrophe(tweet)

		# Remove twitter names like @robpost
		if(choices['pre_remove_twitter_names']['value'] == 1):
			from generalPreprocessingMethods import removeTwitterNames
			tweet = removeTwitterNames(tweet)

		# remove character repetitions. 
		# Example pleeeeeeeeeeeease => please
		# of the rest part will take care the
		# word corrector
		if(choices['pre_repetitions']['value'] == 1):
			from generalPreprocessingMethods import removeCharacterRepetitions
			tweet = removeCharacterRepetitions(tweet)

		# pre-normilize. (imported code) external code, handles some case
		# According to the source of the code:
		# "#Twitter text comes HTML-escaped, so unescape it.
		# We also first unescape &amp;'s, in case the text has been buggily double-escaped."
		if(choices['pre_normalize']['value'] == 1):
			from twokenize import normalizeTextForTagger
			tweet = normalizeTextForTagger(tweet)

		# Tokenize! This tokenizer understands emoticons, urls, anotations,
		# hashtags. Repeated the import statement just show where methods
		# come from
		tweet_tokens = []
		if(choices['pre_tokenize']['value'] == 1):
			from twokenize import tokenizeRawTweetText
			tweet_tokens = tokenizeRawTweetText(tweet)

		####################################################################
		#	MAPPINGS SECTION

		from twokenize import tokenizeRawTweetText

		# map emoticons to positive, negative and neutral (unknown)
		if(choices['pre_map_emoticons']['value'] == 1):
			from mappingFunctions import mapEmoticons
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapEmoticons(token))


		# map brands to a brand key word
		if(choices['pre_map_brands']['value'] == 1):
			tweet_tokens = tokenizeRawTweetText(tweet)
			from mappingFunctions import mapBrands
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapBrands(token))


		# slang mapping
		if(choices['pre_map_slang']['value'] == 1):
			from mappingFunctions import mapSlangs
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapSlangs(token))
				
				


		# map urls to url key word
		if(choices['pre_map_url']['value'] == 1):
			from mappingFunctions import mapURL
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapURL(token))


		# map images to image key word
		#if(choices['pre_map_image']['value'] == 1):
		
		# map hashtags
		if(choices['pre_map_hastags']['value'] == 1):
			from mappingFunctions import mapHashtag
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapHashtag(token))



		# map anotations
		if(choices['pre_map_anotations']['value'] == 1):
			from mappingFunctions import mapAnnotation
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapAnnotation(token))



		# map time
		#if(choices['pre_map_time']['value'] == 1):

		# map date
		#if(choices['pre_map_date']['value'] == 1):

		# map iterjections
		#if(choices['pre_map_iterjections']['value'] == 1):

		#	END OF MAPPING SECTION
		####################################################################


		####################################################################
		#STEMMERS SECTION
		if(choices['pre_stemmer_regexp']['value'] == 1):
			from stemmer import stemmer_regexp
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, stemmer_regexp(token))


		if(choices['pre_stemmer_wordnet']['value'] == 1):
			from stemmer import stemmer_wordnet
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, stemmer_wordnet(token))


		if(choices['pre_stemmer_lancaster']['value'] == 1):
			from stemmer import stemmer_lancaster
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, stemmer_lancaster(token))

		


		# morphing
		if(choices['pre_morphing_wordnet']['value'] == 1):
			from nltk.corpus import wordnet as wn
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:

				word = wn.morphy(token)
				if (str(word).strip() != 'None'):
					tweet = tweet.replace(token, word)
						
					
				

		#END OF STEMMERS SECTION
		####################################################################

		# grammar corrector
		
		if(choices['pre_automated_gramma_corector']['value'] == 1):
			from grammarFixer import correct
			from nltk import word_tokenize
			from nltk.tokenize import RegexpTokenizer
			tokenizer = RegexpTokenizer(r'\w+')
			tweet_temp = tweet

			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				if (token[:2] == '*&'):
					tweet_temp = tweet_temp.replace(token, '')

			tweet_tokens = tokenizer.tokenize(tweet_temp)
			for token in tweet_tokens:
				# remove punctuation
				token 
				token_temp = correct(token)
				if token_temp != token:
					tweet = tweet.replace(token, token_temp)
		

		#print ('\n' + tweet)
		#print('====================================================')


		tweet_list[key] = tweet

	pipeline_tools.statusbar(1, 'Preprocessing')

	return tweet_list
