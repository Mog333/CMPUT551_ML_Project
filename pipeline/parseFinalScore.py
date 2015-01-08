f = open("finalScore.txt",'r')
contents = f.read()
output = open("finalScore2.txt", "w")

for numString in contents.split("]"):
    if numString == '':
        continue
    num = round(float(numString[1:]))
    output.write(str(num) + "\n")
output.close()
f.close()


