
f = open("testResults.txt", "r")
output = open("finalTweets.txt", "w")
for line in f:
    l = line.split("\t")
    output.write(l[1])
output.close()
f.close()
    
