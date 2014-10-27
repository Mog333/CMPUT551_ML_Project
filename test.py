#! /usr/bin/env python

#import re
import numpy as np


in_file = open("small_data.txt", 'r')

words = ""

first = 0
for line in in_file:
   if first == 0: # don't want a space in front of the first word
      words += (''.join(line.split('\t')[3]))
      first = 1
   else:
      words += (' ' + ''.join(line.split('\t')[3]))



words = words.replace('  ', ' ')
words = words.replace(',', "")
words = words.replace('.', '')
words = words.replace('!', '')
words = words.replace('\'', '')
words = words.replace('\"', '')
words = words.replace('\n', '')



all_words = words.split(' ')
all_words_lower = []
# make sure every word is lower case. Smart thing to do in general??
for word in all_words:
   all_words_lower.append(word.lower())

all_words = all_words_lower

# now that all the words have been parsed, we make a dictionary
# with key = word, value = number of times word appeared

bag_dict = {}

featureWords = []

counter_unique = 0
counter_total = 0
for word in all_words:
   #print(word)
   counter_total = counter_total + 1

   if word in bag_dict:
      bag_dict[word] = bag_dict[word] + 1
      #print(word + " " + str(bag_dict[word]))
   else:
      bag_dict[word] = 1
      counter_unique = counter_unique + 1
      featureWords.append(word) # featureWords only contains each word once


''' now that the dictionary is made, we can form our feature vectors
for this test right now, I am making the vector out of the entire dictionary
but when we do it for real, there should be a dictionary for each tweet, with a key
for each word in the entire dataset. (If I know what I am talking about) -Adam
'''

featureVec = np.array([])
for word in featureWords:
   featureVec = np.append(featureVec, bag_dict[word])



'''
bag = []

# add index and counter
for word in all_words:
   entry = []
   entry.append(counter)
   entry.append(word)
   entry.append(0)
   bag.append(entry)
   counter = counter + 1
'''


"""
for word in words:
   for line in all_words:
      if word 
"""

#print bag_dict

#print words

print("=====================")
in_file.close()

print(bag_dict)

print(all_words)
print(featureVec)
print("total number of words = " + str(counter_total))
print("total number of unique words = " + str(counter_unique))

print ("Finish!")

