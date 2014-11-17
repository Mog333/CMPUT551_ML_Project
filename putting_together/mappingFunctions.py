# -*- coding: utf-8 -*-

from __future__ import print_function
import operator

def regex_or(*items):
    return '(?:' + '|'.join(items) + ')'

# This file contains mapping functions

# this function takes as arguemnt a token and
# and determines whather the argument is
# and sad or happhy emoticons by analyzing the
# type of the month that the emoticon has 
#
# the code from this function is take from:
#
# https://github.com/myleott/ark-twokenize-py/blob/master/twokenize.py
#
# and was reused to determine the sentiment of
# emoticon
#
def mapEmoticons(token):
	
	import re

	happyMouths = r"[D\)\]\}]+"
	sadMouths = r"[\(\[\{]+"
	otherMouths = r"(?:[oO]+|[/\\]+|[vV]+|[Ss]+|[|]+)" 


	normalEyes = "[:=]" # 8 and x are eyes but cause problems
	wink = "[;]"
	noseArea = "(?:|-|[^a-zA-Z0-9 ])" # doesn't get :'-(
	tongue = "[pPd3]+"

	bfLeft = u"(♥|0|[oO]|°|[vV]|\\$|[tT]|[xX]|;|\u0ca0|@|ʘ|•|・|◕|\\^|¬|\\*)".encode('utf-8')
	bfCenter = r"(?:[\.]|[_-]+)"
	bfRight = r"\2"
	s3 = r"(?:--['\"])"
	s4 = r"(?:<|&lt;|>|&gt;)[\._-]+(?:<|&lt;|>|&gt;)"
	s5 = "(?:[.][_]+[.])"
	# myleott: in Python the (?i) flag affects the whole expression
	#basicface = "(?:(?i)" +bfLeft+bfCenter+bfRight+ ")|" +s3+ "|" +s4+ "|" + s5
	basicface = "(?:" +bfLeft+bfCenter+bfRight+ ")|" +s3+ "|" +s4+ "|" + s5

	eeLeft = r"[＼\\ƪԄ\(（<>;ヽ\-=~\*]+"
	eeRight= u"[\\-=\\);'\u0022<>ʃ）/／ノﾉ丿╯σっµ~\\*]+".encode('utf-8')
	eeSymbol = r"[^A-Za-z0-9\s\(\)\*:=-]"
	eastEmote = eeLeft + "(?:"+basicface+"|" +eeSymbol+")+" + eeRight

	oOEmote = r"(?:[oO]" + bfCenter + r"[oO])"





	emoticon_pos = regex_or(
        "(?:>|&gt;)?" + regex_or(normalEyes, wink) + regex_or(noseArea,"[Oo]") + regex_or(tongue+r"(?=\W|$|RT|rt|Rt)", happyMouths),
        regex_or("(?<=(?: ))", "(?<=(?:^))") + regex_or(happyMouths) + noseArea + regex_or(normalEyes, wink) + "(?:<|&lt;)?",
        eastEmote.replace("2", "1", 1))



	emoticon_neg = regex_or(
        "(?:>|&gt;)?" + regex_or(normalEyes, wink) + regex_or(noseArea,"[Oo]") + regex_or(tongue+r"(?=\W|$|RT|rt|Rt)", sadMouths),
        regex_or("(?<=(?: ))", "(?<=(?:^))") + regex_or(sadMouths) + noseArea + regex_or(normalEyes, wink) + "(?:<|&lt;)?",
        eastEmote.replace("2", "1", 1))


	emoticon_neutral = regex_or(
        "(?:>|&gt;)?" + regex_or(normalEyes, wink) + regex_or(noseArea,"[Oo]") + regex_or(tongue+r"(?=\W|$|RT|rt|Rt)", otherMouths+r"(?=\W|$|RT|rt|Rt)"),
        regex_or("(?<=(?: ))", "(?<=(?:^))") + regex_or(otherMouths) + noseArea + regex_or(normalEyes, wink) + "(?:<|&lt;)?",
		eastEmote.replace("2", "1", 1), basicface, oOEmote)



	pos_emot = re.compile(unicode(regex_or(emoticon_pos).decode('utf-8')), re.UNICODE)
	neg_emot = re.compile(unicode(regex_or(emoticon_neg).decode('utf-8')), re.UNICODE)
	neutral_emot = re.compile(unicode(regex_or(emoticon_neutral).decode('utf-8')), re.UNICODE)



	from twokenize import splitEdgePunct 
	splitPunctText = splitEdgePunct(token)
	
	for match in pos_emot.finditer(splitPunctText):
		if (match.start() != match.end()):
			#return ("positiveEmoticonKey")
			return 'positive'


	for match in neg_emot.finditer(splitPunctText):
		if (match.start() != match.end()):
			#return ("negativeEmoticonKey")
			return 'negative'


	for match in neutral_emot.finditer(splitPunctText):
		if (match.start() != match.end()):
			#return ("neutralEmoticonKey")
			return'neutral'

	return token




# VERY SLOW -> reading the file content should be outside of
def mapLocations(token):
	# read the content of the file which contains
	# all locations in the world
	locations = []
	f = open('allCitiesAndCountries.txt', 'r')

	for l in f:
		locations.append(l.replace("\n", ''))

	f.close()

	if token in locations:
		return 'locationKey'

	return token




def mapBrands(token):
	brands = []
	f = open('brandList.txt', 'r')

	for b in f:
		brands.append(b.replace("\n", '').replace('\r', ''))

	f.close()

	if token in brands:
		return 'brand'	

	return token



def mapSlangs(token):
	#read from file
	f = open('slang_translator.txt', 'r')

	slang_map = {}
	for line in f:
		line = line.replace('\n', "").replace('\r', '').split('  -  ')
		if (len(line) == 2):
			key = line[0].strip()
			value = line[1].strip()
			slang_map[key] = value
		else:
			
			break

	if token in slang_map:
		return (slang_map[token])

	return token






def mapHashtag(token):
	if token[0] == '#':
		return 'hash'
	return token


def mapAnnotation(token):
	if token[0] == '@':
		return 'annotation'
	return token



"""
symbols = [";(", ";)", ";|", ";D", ";[", 'machine', 'learning']

for s in symbols:
	print (s + " ==> " + mapEmoticons(s))
"""
#print(mapSlangs("tk"))