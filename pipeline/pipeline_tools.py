import sys
import os
from ConfigParser import SafeConfigParser

def buildChoiceArray():
	choices = {}

	###
	# Global
	###
	choices['global'] = {}
	choices['global']['text'] = ''
	choices['global']['pos_values'] = ''
	choices['global']['value'] = -1
	choices['global']['subs'] = ['num_examples','preprocessing','use_unigrams','use_bigrams','cross_val']

	###
	# Number of Examples
	###
	choices['num_examples'] = {}
	choices['num_examples']['text'] = '#Examples'
	choices['num_examples']['pos_values'] = 'int'
	choices['num_examples']['value'] = -1
	choices['num_examples']['subs'] = []

	###
	# Preprocessing
	###
	choices['preprocessing'] = {}
	choices['preprocessing']['text'] = 'Perform preprocessing?'
	choices['preprocessing']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['preprocessing']['value'] = -1
	choices['preprocessing']['subs'] = ['pre_lower_chars','pre_appostrophy','pre_repetitions','pre_normalize','pre_tokenize','pre_map_emoticons','pre_map_brands','pre_map_slang','pre_map_url','pre_map_image','pre_map_hastags','pre_map_anotations','pre_map_time','pre_map_date','pre_map_iterjections']

	# lower characters
	choices['pre_lower_chars'] = {}
	choices['pre_lower_chars']['text'] = 'Lower all characters?'
	choices['pre_lower_chars']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_lower_chars']['value'] = -1
	choices['pre_lower_chars']['subs'] = []

	# normalize words which contain appostrophy
	choices['pre_appostrophy'] = {}
	choices['pre_appostrophy']['text'] = 'Normalize words which contain appostrophy?'
	choices['pre_appostrophy']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_appostrophy']['value'] = -1
	choices['pre_appostrophy']['subs'] = []

	# remove character repetitions. 
	choices['pre_repetitions'] = {}
	choices['pre_repetitions']['text'] = 'Remove character repetitions?'
	choices['pre_repetitions']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_repetitions']['value'] = -1
	choices['pre_repetitions']['subs'] = []

	# pre-normilize. (imported code) external code, handles some case
	# According to the source of the code:
	# "#Twitter text comes HTML-escaped, so unescape it.
	# We also first unescape &amp;'s, in case the text has been buggily double-escaped."
	choices['pre_normalize'] = {}
	choices['pre_normalize']['text'] = 'Pre-normilize (unescape HTML)?'
	choices['pre_normalize']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_normalize']['value'] = -1
	choices['pre_normalize']['subs'] = []

	# pre_tokenize
	choices['pre_tokenize'] = {}
	choices['pre_tokenize']['text'] = 'Tokenize?'
	choices['pre_tokenize']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_tokenize']['value'] = -1
	choices['pre_tokenize']['subs'] = []

	# map emoticons to positive, negative and neutral (unknown)
	choices['pre_map_emoticons'] = {}
	choices['pre_map_emoticons']['text'] = 'Map emoticons to positive, negative and neutral (unknown)?'
	choices['pre_map_emoticons']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_map_emoticons']['value'] = -1
	choices['pre_map_emoticons']['subs'] = []

	# map brands to a brand key word
	choices['pre_map_brands'] = {}
	choices['pre_map_brands']['text'] = 'Map brands to a brand key word?'
	choices['pre_map_brands']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_map_brands']['value'] = -1
	choices['pre_map_brands']['subs'] = []

	# slang mapping
	choices['pre_map_slang'] = {}
	choices['pre_map_slang']['text'] = 'Slang mapping?'
	choices['pre_map_slang']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_map_slang']['value'] = -1
	choices['pre_map_slang']['subs'] = []

	# map urls to url key word
	choices['pre_map_url'] = {}
	choices['pre_map_url']['text'] = 'Map URL?'
	choices['pre_map_url']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_map_url']['value'] = -1
	choices['pre_map_url']['subs'] = []

	# map images to image key word
	choices['pre_map_image'] = {}
	choices['pre_map_image']['text'] = 'Map images?'
	choices['pre_map_image']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_map_image']['value'] = -1
	choices['pre_map_image']['subs'] = []

	# map hashtags
	choices['pre_map_hastags'] = {}
	choices['pre_map_hastags']['text'] = 'Map hashtags?'
	choices['pre_map_hastags']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_map_hastags']['value'] = -1
	choices['pre_map_hastags']['subs'] = []

	# map anotations
	choices['pre_map_anotations'] = {}
	choices['pre_map_anotations']['text'] = 'Map anotations?'
	choices['pre_map_anotations']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_map_anotations']['value'] = -1
	choices['pre_map_anotations']['subs'] = []
	
	# map time
	choices['pre_map_time'] = {}
	choices['pre_map_time']['text'] = 'Map time?'
	choices['pre_map_time']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_map_time']['value'] = -1
	choices['pre_map_time']['subs'] = []

	# map date
	choices['pre_map_date'] = {}
	choices['pre_map_date']['text'] = 'Map date?'
	choices['pre_map_date']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_map_date']['value'] = -1
	choices['pre_map_date']['subs'] = []

	# map iterjections
	choices['pre_map_iterjections'] = {}
	choices['pre_map_iterjections']['text'] = 'Map iterjections?'
	choices['pre_map_iterjections']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['pre_map_iterjections']['value'] = -1
	choices['pre_map_iterjections']['subs'] = []

   	###
	# Feature Creation
	###
	choices['use_unigrams'] = {}
	choices['use_unigrams']['text'] = 'use unigrams?'
	choices['use_unigrams']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['use_unigrams']['value'] = -1
	choices['use_unigrams']['subs'] = ['num_unigram_features']

	choices['num_unigram_features'] = {}
	choices['num_unigram_features']['text'] = 'Number of Unigram Features?'
	choices['num_unigram_features']['pos_values'] = 'int'
	choices['num_unigram_features']['value'] = -1
	choices['num_unigram_features']['subs'] = []

	choices['use_bigrams'] = {}
	choices['use_bigrams']['text'] = 'use bigrams?'
	choices['use_bigrams']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['use_bigrams']['value'] = -1
	choices['use_bigrams']['subs'] = ['num_bigram_features']

	choices['num_bigram_features'] = {}
	choices['num_bigram_features']['text'] = 'Number of bigram Features?'
	choices['num_bigram_features']['pos_values'] = 'int'
	choices['num_bigram_features']['value'] = -1
	choices['num_bigram_features']['subs'] = []


	###
	# Cross Validation
	###
	choices['cross_val'] = {}
	choices['cross_val']['text'] = 'Perform Cross Validation?'
	choices['cross_val']['pos_values'] = {0: 'No', 1: 'Yes'}
	choices['cross_val']['value'] = -1
	choices['cross_val']['subs'] = ['cross_num_folds']

	# Number of Folds
	choices['cross_num_folds'] = {}
	choices['cross_num_folds']['text'] = '#Number of Folds.'
	choices['cross_num_folds']['pos_values'] = 'int'
	choices['cross_num_folds']['value'] = -1
	choices['cross_num_folds']['subs'] = []

	return choices

def ask(choices, questions = '', num = '', parser = ''):
	if(num == ''):
		if(len(sys.argv) >= 2):
			if not os.path.exists(sys.argv[1]):
			    sys.exit('ERROR: Ini %s was not found!' % sys.argv[1])

			parser = SafeConfigParser()
			parser.read('simple.ini')
		else:
			parser = ''
	
	if(questions == ''):
		questions = choices['global']['subs']

	num2 = 1
	for question in questions:
		if( isinstance(choices[question]['pos_values'], str) ):
			pos_values = choices[question]['pos_values']
		else:
			pos_values = ''
			for v in choices[question]['pos_values']:
				# print choice['pos_values'][v]
				pos_values += '[%s: %s]' %(v, choices[question]['pos_values'][v])

		try_ini = 1
		while True:
			print '%s%d) %s (%s)' %(num, num2, choices[question]['text'], pos_values),
			
			if( not isinstance(parser, str) and parser.has_option('choices', question) and try_ini): # get from ini
				v = parser.get('choices', question)
				print '%s (from ini)' % v
				try_ini = 0
			else: # get from user
				v = raw_input()

			if( isinstance(choices[question]['pos_values'], str) ):
				if(choices[question]['pos_values'] == 'int'):
					try:
						int(v)
						break
					except ValueError:
						pass
			else:
				try:
				  choices[question]['pos_values'][int(v)]
				  # print "you entered", choice['pos_values'][int(v)]
				  break
				except KeyError:
					pass
				except ValueError:
					pass

		choices[question]['value'] = int(v)

		
		# print x

		if(len(choices[question]['subs']) and choices[question]['value'] == 1):
			ask(choices, choices[question]['subs'], '  %s%d.' % (num,num2), parser)
		num2 += 1

	return choices

def statusbar(percent, text):
   sys.stdout.write("\r")
   progress = ""
   for i in range(20):
      if i < int(20 * percent):
         progress += "="
      else:
         progress += " "
   sys.stdout.write("%s: [ %s ] %.2f%%" % (text, progress, percent * 100))
   sys.stdout.flush()

   if(percent == 1):
      print ''
