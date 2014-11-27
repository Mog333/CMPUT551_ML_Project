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
			return '*&positive_emoticon'


	for match in neg_emot.finditer(splitPunctText):
		if (match.start() != match.end()):
			#return ("negativeEmoticonKey")
			return '*&negative_emoticon'


	for match in neutral_emot.finditer(splitPunctText):
		if (match.start() != match.end()):
			#return ("neutralEmoticonKey")
			return'*&neutral_emoticon'

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
		return '*&locationKey'

	return token




def mapBrands(token):
	brands = []
	f = open('preprocessing/brandList.txt', 'r')

	for b in f:
		brands.append(b.replace("\n", '').replace('\r', ''))

	f.close()

	if token in brands:
		return '*&brand'	

	return token



def mapSlangs(token):
	#read from file
	f = open('preprocessing/slang_translator.txt', 'r')

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
		return '*&hash'
	return token


def mapAnnotation(token):

	if token[0] == '@':
		return '*&annotation'

	return token




def mapURL(token):
	punctChars = r"['\"“”‘’.?!…,:;]"
	entity     = r"&(?:amp|lt|gt|quot);"
	import re

	urlStart1  = r"(?:https?://|\bwww\.)"
	commonTLDs = r"(?:com|org|edu|gov|net|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|pro|tel|travel|xxx)"
	ccTLDs	 = r"(?:ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|" + \
	r"bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|" + \
	r"er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|" + \
	r"hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|" + \
	r"lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|" + \
	r"nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|" + \
	r"sl|sm|sn|so|sr|ss|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|" + \
	r"va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|za|zm|zw)"	#TODO: remove obscure country domains?
	urlStart2  = r"\b(?:[A-Za-z\d-])+(?:\.[A-Za-z0-9]+){0,3}\." + regex_or(commonTLDs, ccTLDs) + r"(?:\."+ccTLDs+r")?(?=\W|$)"
	urlBody    = r"(?:[^\.\s<>][^\s<>]*?)?"
	urlExtraCrapBeforeEnd = regex_or(punctChars, entity) + "+?"
	urlEnd     = r"(?:\.\.+|[<>]|\s|$)"
	url        = regex_or(urlStart1, urlStart2) + urlBody + "(?=(?:"+urlExtraCrapBeforeEnd+")?"+urlEnd+")"

	url  = re.compile(unicode(regex_or(url).decode('utf-8')), re.UNICODE)

	from twokenize import splitEdgePunct 
	
	splitPunctText = splitEdgePunct(token)
	
	for match in url.finditer(splitPunctText):
		if (match.start() != match.end()):
			#return ("positiveEmoticonKey")
			return '*&link'
	

	return token

"""
symbols = [";(", ";)", ";|", ";D", ";[", 'machine', 'learning']

for s in symbols:
	print (s + " ==> " + mapEmoticons(s))
"""
#print(mapSlangs("tk"))
