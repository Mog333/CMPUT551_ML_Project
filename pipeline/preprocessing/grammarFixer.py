###############################################
#
#	This code is developed by Peter Norvig
# 	and is obtsined from:
#	
#	http://norvig.com/spell-correct.html
#
#
#	The word list file is taken from the 
#	file stored in the linux system
#
#
#


import enchant
d = enchant.Dict("en_US")
#print(str(d.suggest("universit")))



import re, collections

def words(text):
    return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('./preprocessing/big.txt').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts    = [a + c + b     for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or    known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)





def spelltest(tests, bias=None, verbose=False):
    import time
    n, bad, unknown, start = 0, 0, 0, time.clock()
    if bias:
        for target in tests: NWORDS[target] += bias
    for target,wrongs in tests.items():
        for wrong in wrongs.split():
            n += 1
            w = correct(wrong)
            if w!=target:
            	print w
                bad += 1
                unknown += (target not in NWORDS)
                if verbose:
                    print '%r => %r (%d); expected %r (%d)' % (
                        wrong, w, NWORDS[w], target, NWORDS[target])
    return dict(bad=bad, n=n, bias=bias, pct=int(100. - 100.*bad/n), 
                unknown=unknown, secs=int(time.clock()-start) )


#print spelltest(tests1)
"""



"""

# This part is not needed since the
# text corrector is automated, without
# any human inervention
"""

from nltk.stem.porter import *
from nltk.corpus import brown
from nltk import tokenize
 
import sys
from collections import defaultdict
import operator


def sortby(nlist ,n, reverse=0):
    nlist.sort(key=operator.itemgetter(n), reverse=reverse)
 
class mydict(dict):
    def __missing__(self, key):
        return 0
 
class DidYouMean:
    def __init__(self):
        self.stemmer = PorterStemmer()
 
    def specialhash(self, s):
        s = s.lower()
        s = s.replace("z", "s")
        s = s.replace("h", "")
        for i in [chr(ord("a") + i) for i in range(26)]:
            s = s.replace(i+i, i)
        s = self.stemmer.stem(s)
        return s
 
    def test(self, token):
        hashed = self.specialhash(token)
        if hashed in self.learned:
            words = self.learned[hashed].items()
            sortby(words, 1, reverse=1)
            if token in [i[0] for i in words]:
                     else:
                if len(words) == 1:
                    return 'Did you mean "%s" ?' % words[0][0]
                else:
                    return 'Did you mean "%s" ? (or %s)' \
                           % (words[0][0], ", ".join(['"'+i[0]+'"' \
                                                      for i in words[1:]]))
        return "I can't found similar word in my learned db"
 
    def learn(self, listofsentences=[], n=2000):
        self.learned = defaultdict(mydict)
        if listofsentences == []:
            listofsentences = brown.raw()
        for i, sent in enumerate(listofsentences):
            if i >= n: # Limit to the first nth sentences of the corpus
                break
            for word in sent:
                self.learned[self.specialhash(word)][word.lower()] += 1
 

"""
"""
def demo():
    d = DidYouMean()
    d.learn()
    # choice of words to be relevant related to the brown corpus
    for i in "birdd, oklaoma, emphasise, bird, carot, nice, cat".split(", "):
        print i, "-", d.test(i)
 
if __name__ == "__main__":
    demo()
"""
