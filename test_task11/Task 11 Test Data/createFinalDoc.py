scores = open("finalScore2.txt",'r')
ids = open("tes",'r')
output = open("final.csv",'w')

parsing = True
for i in range(0, 4000):
    score = scores.readline().strip()
    scoreID = ids.readline().strip()
    output.write(str(scoreID) + "\t" + str(score) + "\n")

output.close()
ids.close()
scores.close()
