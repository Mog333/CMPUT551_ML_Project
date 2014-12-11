

def g():
	counter = 200
	for use_POStagging in range (0, 2):
		for use_temporalComp in range (0, 2):
			for use_counterFact in range (0, 2):
				for use_sentiment in range (0, 2):

					for pre_drop_stop_words in range (0, 2):
						
						for pre_automated_gramma_corector in range (0, 2):
							for pre_automated_gramma_corector_first in range (0, 2):
								for pre_stemmer_wordnet in range (0, 2):
									#write things
									f = open(str(counter) + ".ini", 'w')
									
									
									s = "[choices]\nnum_examples = 8000\npreprocessing = 1\npre_lower_chars = 1\n"
									s = s + ("pre_appostrophy = 1\n")
									s = s + "pre_repetitions = 0\npre_remove_twitter_names = 0\npre_normalize = 1\n"
									s = s + ("pre_drop_stop_words = " + str(pre_drop_stop_words)+ "\n")
									s = s + "pre_tokenize = 1\n" 
									s = s + ("pre_map_emoticons = 1\n")
									s = s + "pre_map_brands = 0\npre_map_slang = 0\npre_map_url = 1\npre_map_image = 0\npre_map_hastags = 0\npre_map_anotations = 1\npre_map_time = 0\npre_map_date = 0\npre_map_iterjections = 0\npre_stemmer_regexp = 0\n"
									##########
									s = s + ("pre_stemmer_wordnet = " + str(pre_stemmer_wordnet)+ "\n")
									s = s + ("pre_stemmer_lancaster = 0\npre_morphing_wordnet = 0\npre_hypermin_wordnet = 0\n")
									#####
									s = s + ("pre_automated_gramma_corector = " + str(pre_automated_gramma_corector)+ "\n")
									s = s + ("pre_automated_gramma_corector_first = " + str(pre_automated_gramma_corector_first)+ "\n")
									s = s + "use_unigrams = 1\nnum_unigram_features = 200\nuse_bigrams = 0\nnum_bigram_features = 0\n"
									s = s + ("use_sentiment = " + str(use_sentiment)+ "\n")
									s = s + ("use_counterFact = " + str(use_counterFact)+ "\n")
									s = s + ("use_temporalComp = " + str(use_temporalComp)+ "\n")
									s = s + ("use_POStagging = " + str(use_POStagging)+ "\n")
									s = s + "svm_model = 0\nsvm_degree = 3\ncross_val = 1\ncross_num_folds = 5\n"

									f.write(s)
									f.close()
									counter = counter + 1


	for use_POStagging in range (0, 2):
		for use_temporalComp in range (0, 2):
			for use_counterFact in range (0, 2):
				for use_sentiment in range (0, 2):
						for pre_drop_stop_words in range (0, 2):
							
								for pre_automated_gramma_corector in range (0, 2):
									for pre_automated_gramma_corector_first in range (0, 2):
										for pre_stemmer_lancaster in range (0, 2):
											#write things
											f = open(str(counter) + ".ini", 'w')
											
											s = "[choices]\nnum_examples = 8000\npreprocessing = 1\npre_lower_chars = 1\n"
											s = s + ("pre_appostrophy = 1\n")
											s = s + "pre_repetitions = 0\npre_remove_twitter_names = 0\npre_normalize = 1\n"
											s = s + ("pre_drop_stop_words = " + str(pre_drop_stop_words)+ "\n")
											s = s + "pre_tokenize = 1\n" 
											s = s + ("pre_map_emoticons = 1\n")
											s = s + "pre_map_brands = 0\npre_map_slang = 0\npre_map_url = 1\npre_map_image = 0\npre_map_hastags = 0\npre_map_anotations = 1\npre_map_time = 0\npre_map_date = 0\npre_map_iterjections = 0\npre_stemmer_regexp = 0\n"
											##########
											s = s + ("pre_stemmer_wordnet = 0\n")
											s = s + ("pre_stemmer_lancaster = " + str(pre_stemmer_lancaster)+ "\n")
											s = s + ("pre_morphing_wordnet = 0\npre_hypermin_wordnet = 0\n")
											
											#####
											s = s + ("pre_automated_gramma_corector = " + str(pre_automated_gramma_corector)+ "\n")
											s = s + ("pre_automated_gramma_corector_first = " + str(pre_automated_gramma_corector_first)+ "\n")
											s = s + "use_unigrams = 1\nnum_unigram_features = 200\nuse_bigrams = 0\nnum_bigram_features = 0\n"
											s = s + ("use_sentiment = " + str(use_sentiment)+ "\n")
											s = s + ("use_counterFact = " + str(use_counterFact)+ "\n")
											s = s + ("use_temporalComp = " + str(use_temporalComp)+ "\n")
											s = s + ("use_POStagging = " + str(use_POStagging)+ "\n")
											s = s + "svm_model = 0\nsvm_degree = 3\ncross_val = 1\ncross_num_folds = 5\n"

											f.write(s)
											f.close()

											counter = counter + 1										

	for use_POStagging in range (0, 2):
		for use_temporalComp in range (0, 2):
			for use_counterFact in range (0, 2):
				for use_sentiment in range (0, 2):
						for pre_drop_stop_words in range (0, 2):
								for pre_automated_gramma_corector in range (0, 2):
									for pre_automated_gramma_corector_first in range (0, 2):
										for pre_morphing_wordnet in range (0, 2):
											#write things
											f = open(str(counter) + ".ini", 'w')
											
											s = "[choices]\nnum_examples = 8000\npreprocessing = 1\npre_lower_chars = 1\n"
											s = s + ("pre_appostrophy = 1\n")
											s = s + "pre_repetitions = 0\npre_remove_twitter_names = 0\npre_normalize = 1\n"
											s = s + ("pre_drop_stop_words = " + str(pre_drop_stop_words)+ "\n")
											s = s + "pre_tokenize = 1\n" 
											s = s + ("pre_map_emoticons = 1\n")
											s = s + "pre_map_brands = 0\npre_map_slang = 0\npre_map_url = 1\npre_map_image = 0\npre_map_hastags = 0\npre_map_anotations = 1\npre_map_time = 0\npre_map_date = 0\npre_map_iterjections = 0\npre_stemmer_regexp = 0\n"
											##########
											s = s + ("pre_stemmer_wordnet = 0\npre_stemmer_lancaster = 0\n")
											s = s + ("pre_morphing_wordnet = " + str(pre_morphing_wordnet)+ "\n")
											s = s + ("pre_hypermin_wordnet = 0\n")
											#####
											s = s + ("pre_automated_gramma_corector = " + str(pre_automated_gramma_corector)+ "\n")
											s = s + ("pre_automated_gramma_corector_first = " + str(pre_automated_gramma_corector_first)+ "\n")
											s = s + "use_unigrams = 1\nnum_unigram_features = 200\nuse_bigrams = 0\nnum_bigram_features = 0\n"
											s = s + ("use_sentiment = " + str(use_sentiment)+ "\n")
											s = s + ("use_counterFact = " + str(use_counterFact)+ "\n")
											s = s + ("use_temporalComp = " + str(use_temporalComp)+ "\n")
											s = s + ("use_POStagging = " + str(use_POStagging)+ "\n")
											s = s + "svm_model = 0\nsvm_degree = 3\ncross_val = 1\ncross_num_folds = 5\n"

											f.write(s)
											f.close()
											
											counter = counter + 1

	for use_POStagging in range (0, 2):
		for use_temporalComp in range (0, 2):
			for use_counterFact in range (0, 2):
				for use_sentiment in range (0, 2):
					
						for pre_drop_stop_words in range (0, 2):
							
								for pre_automated_gramma_corector in range (0, 2):
									for pre_automated_gramma_corector_first in range (0, 2):
										for pre_hypermin_wordnet in range (0, 2):
											#write things
											f = open(str(counter) + ".ini", 'w')
											
											s = "[choices]\nnum_examples = 8000\npreprocessing = 1\npre_lower_chars = 1\n"
											s = s + ("pre_appostrophy = 1\n")
											s = s + "pre_repetitions = 0\npre_remove_twitter_names = 0\npre_normalize = 1\n"
											s = s + ("pre_drop_stop_words = " + str(pre_drop_stop_words)+ "\n")
											s = s + "pre_tokenize = 1\n" 
											s = s + ("pre_map_emoticons = 1\n")
											s = s + "pre_map_brands = 0\npre_map_slang = 0\npre_map_url = 1\npre_map_image = 0\npre_map_hastags = 0\npre_map_anotations = 1\npre_map_time = 0\npre_map_date = 0\npre_map_iterjections = 0\npre_stemmer_regexp = 0\n"
											##########
											
											s = s + ("pre_stemmer_wordnet = 0\npre_stemmer_lancaster = 0\npre_morphing_wordnet = 0\n")
											s = s + ("pre_hypermin_wordnet = " + str(pre_hypermin_wordnet)+ "\n")
											#####
											s = s + ("pre_automated_gramma_corector = " + str(pre_automated_gramma_corector)+ "\n")
											s = s + ("pre_automated_gramma_corector_first = " + str(pre_automated_gramma_corector_first)+ "\n")
											s = s + "use_unigrams = 1\nnum_unigram_features = 200\nuse_bigrams = 0\nnum_bigram_features = 0\n"
											s = s + ("use_sentiment = " + str(use_sentiment)+ "\n")
											s = s + ("use_counterFact = " + str(use_counterFact)+ "\n")
											s = s + ("use_temporalComp = " + str(use_temporalComp)+ "\n")
											s = s + ("use_POStagging = " + str(use_POStagging)+ "\n")
											s = s + "svm_model = 0\nsvm_degree = 3\ncross_val = 1\ncross_num_folds = 5\n"

											f.write(s)
											f.close()
											
											counter = counter + 1
def main():
	g()


main()