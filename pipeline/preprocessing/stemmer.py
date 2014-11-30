#! /usr/bin/env python


def stemmer_regexp(token):
	from nltk.stem import RegexpStemmer
	st_reg = RegexpStemmer('ing$|s$|able$|\'s', min=4)
	return(st_reg.stem(token))





def stemmer_wordnet(token):
	from nltk.stem import WordNetLemmatizer
	wnl = WordNetLemmatizer()
	return(wnl.lemmatize(token))





def stemmer_lancaster(token):
	from nltk.stem.lancaster import LancasterStemmer
	stemmer = LancasterStemmer()	
	return(stemmer.stem(token))



def morphing_wordnet(token):
	from nltk.corpus import wordnet as wn
	word = wn.morphy(token)
	if (str(word).strip() != 'None'):
		return word
	else:
		token


def hypermin_wordnet(token):
	from nltk.corpus import wordnet as wn
	word = wn.synsets(token)
	if (len(word) > 0):
		hypernym = word[0].hypernyms()
		if (len(hypernym) > 0):
			#print (token + "\t\t===>\t\t" + (str(hypernym[0]).replace('Synset(\'', '').replace('\')', '').split('.')[0]))
			return (str(hypernym[0]).replace('Synset(\'', '').replace('\')', '').split('.')[0])
	
	return token




"""
# autmomated spelling mistakes corrector
from grammarFixer import correct


tokens = ['reading', 'computer', 'computer', 'taking', 'unsolved',
	'resolution', 'investigating', 'abbreviated', 'transversal', 
	'originated', 'tentacles']
for token in tokens:
	print('Original\t\t' + token)
	t1 = stemmer_regexp(token)
	print("regex\t=> \t" + t1 + "\t\t" + correct(t1))
	t2 = stemmer_wordnet(token)
	print('wordnet\t=> \t' + t2 + "\t\t" + correct(t2))
	t3 = stemmer_lancaster(token)
	print('lankaster\t=> \t' + t3 + "\t\t" + correct(t3))
	t4 = morphing_wordnet(token)
	print('morthing\t=> \t' + t4  + "\t\t" + correct(t4))



	print('=============================')

"""