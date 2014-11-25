import pipeline_tools

def preprocess(tweet_list, choices):
	
	for key,tweet in enumerate(tweet_list):
		percent = 1.0 * key / len(tweet_list)
		pipeline_tools.statusbar(percent, 'Preprocessing')

		# lower case
		if(choices['pre_lower_chars']['value'] == 1):
			tweet = tweet.lower()

		# normalize words which contain appostrophy
		# as ommission character
		if(choices['pre_appostrophy']['value'] == 1):
			from generalPreprocessingMethods import removeApostrophe
			tweet = removeApostrophe(tweet)

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
		if(choices['pre_tokenize']['value'] == 1):
			from twokenize import tokenizeRawTweetText
			tweet_tokens = tokenizeRawTweetText(tweet)

		####################################################################
		#	MAPPINGS SECTION

		# map emoticons to positive, negative and neutral (unknown)
		if(choices['pre_map_emoticons']['value'] == 1):
			from mappingFunctions import mapEmoticons
			tokens_temp = []
			for token in tweet_tokens:
				tokens_temp.append(mapEmoticons(token))

			tweet_tokens = tokens_temp

		# map brands to a brand key word
		if(choices['pre_map_brands']['value'] == 1):
			from mappingFunctions import mapBrands
			tokens_temp = []
			for token in tweet_tokens:
				tokens_temp.append(mapBrands(token))

			tweet_tokens = tokens_temp


		# slang mapping
		if(choices['pre_map_slang']['value'] == 1):
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
		#if(choices['pre_map_url']['value'] == 1):


		# map images to image key word
		#if(choices['pre_map_image']['value'] == 1):
		
		# map hashtags
		if(choices['pre_map_hastags']['value'] == 1):
			from mappingFunctions import mapHashtag
			tokens_temp = []
			for token in tweet_tokens:
				tokens_temp.append(mapHashtag(token))

			tweet_tokens = tokens_temp

		# map anotations
		if(choices['pre_map_anotations']['value'] == 1):
			from mappingFunctions import mapAnnotation
			tokens_temp = []
			for token in tweet_tokens:
				tokens_temp.append(mapAnnotation(token))

			tweet_tokens = tokens_temp

		# map time
		#if(choices['pre_map_time']['value'] == 1):

		# map date
		#if(choices['pre_map_date']['value'] == 1):

		# map iterjections
		#if(choices['pre_map_iterjections']['value'] == 1):

		#	END OF MAPPING SECTION
		####################################################################

	pipeline_tools.statusbar(1, 'Preprocessing')

	return tweet_list