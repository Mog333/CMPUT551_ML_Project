
def reduceFile():
	liwc = open('liwc.txt', 'r')
	new_liwc = open('liwc_reduced.txt', 'w')

	for line in liwc:
		lineData = line.split()
		if '27' in lineData:
			new_liwc.write(lineData[0] + ' 27\n')
		if '28' in lineData:
			new_liwc.write(lineData[0] + ' 28\n')
	
	new_liwc.close()
	liwc.close()
