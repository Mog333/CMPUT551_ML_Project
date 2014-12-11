
def findBestResult(filename):
	f = open(filename, 'r')
	minVal = 2.0
	minIni = 0.0
	for line in f:
		print(line)
		res = line.split(",")
		if float(res[6]) < minVal:
			minIni = res[0]
			minVal = res[6]
	print("Min score: " + str(minVal) + " at ini: " + str(minIni))
	f.close()

if __name__ == "__main__":
	findBestResult("output_500_800.csv")
