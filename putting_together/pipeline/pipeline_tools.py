import sys
import os
from ConfigParser import SafeConfigParser

def buildChoiceArray():
	choices = []


	###
	# Number of Examples
	###
	tmp = {}
	tmp['name'] = 'num_examples'
	tmp['text'] = '#Examples'
	tmp['pos_values'] = {0: '50', 1: '100', 2: '500', 3: '1500', 4: '8000'}
	tmp['value'] = -1
	tmp['subs'] = []
	choices.append(tmp)

	###
	# Preprocessing
	###
	tmp = {}
	tmp['name'] = 'preprocessing'
	tmp['text'] = 'Perform preprocessing?'
	tmp['pos_values'] = {0: 'No', 1: 'Yes'}
	tmp['value'] = -1
	tmp['subs'] = []

	# lower characters
	tmp2 = {}
	tmp2['name'] = 'lower_chars'
	tmp2['text'] = 'Lower all characters?'
	tmp2['pos_values'] = {0: 'No', 1: 'Yes'}
	tmp2['value'] = -1
	tmp2['subs'] = []
	tmp['subs'].append(tmp2)

	# normalize words which contain appostrophy
	tmp2 = {}
	tmp2['name'] = 'appostrophy'
	tmp2['text'] = 'Normalize words which contain appostrophy?'
	tmp2['pos_values'] = {0: 'No', 1: 'Yes'}
	tmp2['value'] = -1
	tmp2['subs'] = []
	tmp['subs'].append(tmp2)

	# remove character repetitions. 
	tmp2 = {}
	tmp2['name'] = 'repetitions'
	tmp2['text'] = 'Remove character repetitions?'
	tmp2['pos_values'] = {0: 'No', 1: 'Yes'}
	tmp2['value'] = -1
	tmp2['subs'] = []
	tmp['subs'].append(tmp2)

	# pre-normilize. (imported code) external code, handles some case
	# According to the source of the code:
	# "#Twitter text comes HTML-escaped, so unescape it.
	# We also first unescape &amp;'s, in case the text has been buggily double-escaped."
	tmp2 = {}
	tmp2['name'] = 'pre_normilize'
	tmp2['text'] = 'Pre-normilize (unescape HTML)?'
	tmp2['pos_values'] = {0: 'No', 1: 'Yes'}
	tmp2['value'] = -1
	tmp2['subs'] = []
	tmp['subs'].append(tmp2)

	choices.append(tmp)

	###
	# Cross Validation
	###
	tmp = {}
	tmp['name'] = 'cross_val'
	tmp['text'] = 'Perform Cross Validation?'
	tmp['pos_values'] = {0: 'No', 1: 'Yes'}
	tmp['value'] = -1
	tmp['subs'] = []

	# Number of DataPoints
	tmp2 = {}
	tmp2['name'] = 'num_DataPoints'
	tmp2['text'] = '#DataPoints.'
	tmp2['pos_values'] = 'int'
	tmp2['value'] = -1
	tmp2['subs'] = []
	tmp['subs'].append(tmp2)

	# Number of Folds
	tmp2 = {}
	tmp2['name'] = 'Num_folds'
	tmp2['text'] = '#Number of Folds.'
	tmp2['pos_values'] = 'int'
	tmp2['value'] = -1
	tmp2['subs'] = []
	tmp['subs'].append(tmp2)

	choices.append(tmp)

	return choices

def ask(choices, num = '', parser = ''):
	if(num == ''):
		if(len(sys.argv) >= 2):
			if not os.path.exists(sys.argv[1]):
			    sys.exit('ERROR: Ini %s was not found!' % sys.argv[1])

			parser = SafeConfigParser()
			parser.read('simple.ini')
		else:
			parser = ''
	# print type(parser)
	# print not isinstance(parser, str)
	num2 = 1
	for choice in choices:
		if( isinstance(choice['pos_values'], str) ):
			pos_values = choice['pos_values']
		else:
			pos_values = ''
			for v in choice['pos_values']:
				# print choice['pos_values'][v]
				pos_values += '[%s: %s]' %(v, choice['pos_values'][v])

		try_ini = 1
		while True:
			print '%s%d) %s (%s)' %(num, num2, choice['text'], pos_values),
			
			if( not isinstance(parser, str) and parser.has_option('choices', choice['name']) and try_ini): # get from ini
				v = parser.get('choices', choice['name'])
				print '%s (from ini)' % v
				try_ini = 0
			else: # get from user
				v = raw_input()

			if( isinstance(choice['pos_values'], str) ):
				if(choice['pos_values'] == 'int'):
					try:
						int(v)
						break
					except ValueError:
						pass
			else:
				try:
				  choice['pos_values'][int(v)]
				  # print "you entered", choice['pos_values'][int(v)]
				  break
				except KeyError:
					pass
				except ValueError:
					pass

		choice['value'] = int(v)

		
		# print x

		if(len(choice['subs']) and choice['value'] == 1):
			choice['subs'] = ask(choice['subs'], '  %s%d.' % (num,num2), parser)
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