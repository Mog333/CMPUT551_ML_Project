import numpy as np
import subprocess
import os

temp = os.system('./runTagger.sh --output-format conll tweet.txt >out.txt')

f = open("out.txt",'r')
f1 = open("postTagged.txt",'w+')
f2 = open("tagged_tweets.txt",'w+')

array = [];

for line in f:
	if(line=='\n'):
		f1.write('\n')
		f2.write('\n')
		continue
	line = line.replace('\n','')
	line = line.split('\t')
	#print(line[0])
	#print(line[1])
	#print(line[2])
	#print('\n')	
	if(float(line[2])>.9 and line[1] in ('O','N','^','V','A','R','D','P','#','@','~','U','E',',','!')):
		#print(line)
		if(line[1]=='O'):
			f2.write('*&O ')
		if(line[1]=='N'):
			f2.write('*&N ')
		if(line[1]=='^'):
			f2.write('*&^ ')
		if(line[1]=='V'):
			f2.write('*&V ')
		if(line[1]=='A'):
			f2.write('*&A ')
		if(line[1]=='R'):
			f2.write('*&R ')
		if(line[1]=='D'):
			f2.write('*&D ')
		if(line[1]=='P'):
			f2.write('*&P ')
		if(line[1]=='#'):
			f2.write('*&# ')
		if(line[1]=='@'):
			f2.write('*&@ ')
		if(line[1]=='~'):
			f2.write('*&~ ')
		if(line[1]=='U'):
			f2.write('*&U ')
		if(line[1]=='E'):
			f2.write('*&E ')
		if(line[1]==','):
			f2.write('*&, ')
		if(line[1]=='!'):
			f2.write('*&! ')													
		line = " ".join(line)
		#print(line)
		f1.write(line)
		f1.write('\n')


f4 = open("tweet.txt",'r')
f2.seek(0,0)

f5 = open("TaggedTweets.txt",'w')

lines1 = f4.readlines()
lines2 = f2.readlines()

for i in range(len(lines1)):
	line1 = lines1[i]
	f5.write(line1)
	line2 = lines2[i]
	f5.write(line2)
	f5.write('\n')


