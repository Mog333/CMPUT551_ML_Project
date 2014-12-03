import numpy as np
import subprocess
import os

temp = os.system('./runTagger.sh --output-format conll tweet.txt >out.txt')

f = open("out.txt",'r')
f2 = open("tagged_tweets.txt",'w')
f3 = open("tweet.txt", 'r')

lines = f3.readlines()

tags = []
tweet = []
count = 0

for line in f:
	if(line=='\n'):
		tweet = lines[count]
		tweet = tweet.split(" ")
		tweet[-1] = tweet[-1].strip()
		tweet = (" ").join(tweet + tags)
		count+=1
		f2.write(tweet)
		f2.write('\n')
		tags = []
		tweet = []
		continue	
	line = line.replace('\n','')
	line = line.split('\t')
	if(float(line[2])>.9 and line[1] in ('O','N','^','V','A','R','D','P','#','@','~','U','E',',','!')):
		if(line[1]=='O'):
			#f2.write('*&O ')
			tags.append('*&O')
		if(line[1]=='N'):
			#f2.write('*&N ')
			tags.append('*&N')
		if(line[1]=='^'):
			#f2.write('*&^ ')
			tags.append('*&^')
		if(line[1]=='V'):
			#f2.write('*&V ')
			tags.append('*&V')
		if(line[1]=='A'):
			#f2.write('*&A ')
			tags.append('*&A')
		if(line[1]=='R'):
			#f2.write('*&R ')
			tags.append('*&R')
		if(line[1]=='D'):
			#f2.write('*&D ')
			tags.append('*&D')
		if(line[1]=='P'):
			#f2.write('*&P ')
			tags.append('*&P')
		if(line[1]=='#'):
			#f2.write('*&# ')
			tags.append('*&#')
		if(line[1]=='@'):
			#f2.write('*&@ ')
			tags.append('*&@')
		if(line[1]=='~'):
			#f2.write('*&~ ')
			tags.append('*&~')
		if(line[1]=='U'):
			#f2.write('*&U ')
			tags.append('*&U')
		if(line[1]=='E'):
			#f2.write('*&E ')
			tags.append('*&E')
		if(line[1]==','):
			#f2.write('*&, ')
			tags.append('*&,')
		if(line[1]=='!'):
			#f2.write('*&! ')
			tags.append('*&!')



