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


		
		if(choices['pre_drop_stop_words']['value'] == 1):
			from nltk.corpus import stopwords
			stopset = set(stopwords.words('english'))
			from twokenize import tokenizeRawTweetText
			
			token_list = tokenizeRawTweetText(tweet)
			token_temp = []

			for token in token_list:
				if token not in stopset:
					token_temp.append(token)
				else:
					# in order to satisfy req for token_replacer
					# which is that token_list token_temp must 
					# have equal length
					token_temp.append(' ')

			tweet = token_replacer(tweet, token_list, token_temp)
		


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

		


		# map brands to a brand key word
		if(choices['pre_map_brands']['value'] == 1):
			from twokenize import tokenizeRawTweetText
			tweet_tokens = tokenizeRawTweetText(tweet)
			from mappingFunctions import mapBrands
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapBrands(token))


		# slang mapping
		if(choices['pre_map_slang']['value'] == 1):
			from twokenize import tokenizeRawTweetText
			from mappingFunctions import mapSlangs
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapSlangs(token))
				
				


		# map urls to url key word
		if(choices['pre_map_url']['value'] == 1):
			from twokenize import tokenizeRawTweetText
			from mappingFunctions import mapURL
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapURL(token))


		# map emoticons to positive, negative and neutral (unknown)
		if(choices['pre_map_emoticons']['value'] == 1):
			from mappingFunctions import mapEmoticons
			from twokenize import tokenizeRawTweetText
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapEmoticons(token))

		
		# map images to image key word
		#if(choices['pre_map_image']['value'] == 1):
		
		# map hashtags
		if(choices['pre_map_hastags']['value'] == 1):
			from twokenize import tokenizeRawTweetText
			from mappingFunctions import mapHashtag
			tweet_tokens = tokenizeRawTweetText(tweet)
			for token in tweet_tokens:
				tweet = tweet.replace(token, mapHashtag(token))



		# map anotations
		if(choices['pre_map_anotations']['value'] == 1):
			from twokenize import tokenizeRawTweetText
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
		if((choices['pre_automated_gramma_corector']['value'] == 1) and 
			(choices['pre_automated_gramma_corector_first']['value'] == 1)):
			do_automated_gramma_corector(tweet)
			


		if(choices['pre_stemmer_regexp']['value'] == 1):
			from twokenize import tokenizeRawTweetText
			from stemmer import stemmer_regexp

			token_list = tokenizeRawTweetText(tweet)
			token_temp = []

			for token in token_list:
				if ((token[0:2] == '*@#') or (token[0] == '#') or (token[0] == '@' )):
					token_temp.append(token)
				else:
					token_temp.append(stemmer_regexp(token))

			tweet = token_replacer(tweet, token_list, token_temp)




		if(choices['pre_stemmer_wordnet']['value'] == 1):
			from stemmer import stemmer_wordnet
			from twokenize import tokenizeRawTweetText

			token_list = tokenizeRawTweetText(tweet)
			token_temp = []

			for token in token_list:
				if ((token[0:2] == '*@#') or (token[0] == '#') or (token[0] == '@' )):
					token_temp.append(token)
				else:
					token_temp.append(stemmer_wordnet(token))

			tweet = token_replacer(tweet, token_list, token_temp)



		if(choices['pre_stemmer_lancaster']['value'] == 1):
			from stemmer import stemmer_lancaster
			from twokenize import tokenizeRawTweetText

			token_list = tokenizeRawTweetText(tweet)
			token_temp = []

			for token in token_list:
				if ((token[0:2] == '*@#') or (token[0] == '#') or (token[0] == '@' )):
					token_temp.append(token)
				else:
					token_temp.append(stemmer_lancaster(token))

			tweet = token_replacer(tweet, token_list, token_temp)


		


		# morphing
		if(choices['pre_morphing_wordnet']['value'] == 1):
			from nltk.corpus import wordnet as wn
			from twokenize import tokenizeRawTweetText
			tweet_tokens = tokenizeRawTweetText(tweet)

			token_list = tokenizeRawTweetText(tweet)
			token_temp = []

			for token in token_list:
				if ((token[0:2] == '*@#') or (token[0] == '#') or (token[0] == '@' )):
					token_temp.append(token)
				else:
					word = wn.morphy(token)
					if (str(word).strip() != 'None'):
						token_temp.append(word)
					else:
						token_temp.append(token)

			tweet = token_replacer(tweet, token_list, token_temp)


				
						

					
		#hypernims
		if(choices['pre_hypermin_wordnet']['value'] == 1):
			from stemmer import hypermin_wordnet
			from nltk import word_tokenize
			from nltk.tokenize import RegexpTokenizer
			from twokenize import tokenizeRawTweetText

			token_list = tokenizeRawTweetText(tweet)
			token_temp = []

			for token in token_list:
				if ((token[0:2] == '*@#') or (token[0] == '#') or (token[0] == '@' )):
					token_temp.append(token)
				else:
					token_temp.append(hypermin_wordnet(token))

			tweet = token_replacer(tweet, token_list, token_temp)
		
		if((choices['pre_automated_gramma_corector']['value'] == 1) and 
			(choices['pre_automated_gramma_corector_first']['value'] == 0)):
			do_automated_gramma_corector(tweet)
			

		#END OF STEMMERS SECTION
		####################################################################

		
		

		#print ('\n' + tweet)
		#print('====================================================')


		tweet_list[key] = tweet

	pipeline_tools.statusbar(1, 'Preprocessing')

	return tweet_list




def token_replacer(tweet, t_ini, t_fin):
	
	tweet_final = ""
	counter = 0
	while (len(tweet) > 0):
		pos_start = tweet.find(t_ini[counter])
		
		# check if the token is not set to the special character
		if ((t_ini[counter][0:2] == '*@#') or (t_ini[counter][0] == '#') or (t_ini[counter][0] == '@' )):
			tweet_final += tweet[0:pos_start] + t_ini[counter]
		else:
			# add to the new tweet everything what was before the token
			tweet_final += tweet[0:pos_start] + t_fin[counter]
			
		tweet = tweet[pos_start + len(t_ini[counter]): ]

		counter += 1
		if (counter == len(t_ini)):
			tweet_final += tweet.replace(t_ini[counter - 1], "")
			tweet = ""
		
	return tweet_final


def do_automated_gramma_corector(tweet):
	from grammarFixer import correct
	from nltk import word_tokenize
	from nltk.tokenize import RegexpTokenizer
	from twokenize import tokenizeRawTweetText
	tokenizer = RegexpTokenizer(r'\w+')
	tweet_temp = tweet

	tweet_tokens = tokenizeRawTweetText(tweet)
	for token in tweet_tokens:
		if ((token[:2] == '*@#') or (token[:1] == '#')):
			tweet_temp = tweet_temp.replace(token, '')

	tweet_tokens = tokenizer.tokenize(tweet_temp)
	for token in tweet_tokens:
		# remove punctuation
				
		token_temp = correct(token)
		if token_temp != token:
			tweet = tweet.replace(token, token_temp)

	return tweet