import sys
import random
import numpy
from scipy import spatial

class Document:
    """Represents an HTML document"""
    def __init__(self, url):
        self.url = url
        self.outbound = []
        self.inbound = []
        self.outboundcount = 0
        self.inboundcount = 0
        self.pagerank = 0.25
        self.visibility = 0
        self.position = 0
        self.count = 0
        self.depth = 0;

def processDocuments(documents, inputFileName):
    print("reading from input file...")
    inputFile = open(inputFileName, "r")
    for line in inputFile:
        if line.find("   ") != 0:
            documents[line[:-2]] = (Document(line[:-2]))
        elif line[3:-9] not in documents:
        	documents[line[3:-9]] = (Document(line[3:-9]))

    inputFile = open(inputFileName, "r")
    for line in inputFile:
        if line.find("   ") == 0:
        	documents[line[3:-9]].visibility += int(line[-2:-1])
        	documents[line[3:-9]].position += int(line[-6:-5])
        	documents[line[3:-9]].count += 1


def usermat(inputfilename,documents):
	inputFile = open(inputfilename, "r")
	data = inputFile.read()
	num_lines = sum(1 for line in open(inputfilename))
	print num_lines
	w, h = 4, num_lines 
	#User_Matrix = [[0.00 for x in xrange(w)] for y in xrange(h)] 
	User_Matrix = numpy.zeros(shape=(5,num_lines+1),dtype=object)
	#print User_Matrix
	data_array = data.split('\n')
	for i in range(num_lines):
		User_Matrix[0][i + 1] = (':'.join(data_array[i].split(':')[0:2]))
	for i in range(1,5):
		User_Matrix[i][0] = 'User' + str(i)

	inputFile = open(inputfilename, "r")
	metaurl = []
	for line in inputFile:
		metaurl.append(':'.join(line.split(':')[0:2]))

	visibility = float(random.randint(1, 3))/3.00
	position = float(random.randint(1, 2))/2.00
	freshness = float(random.randint(1, 10))/10.00
	visittime = float(random.randint(1, 600))/600.00
	visitfrequency = float(random.randint(1, 50))/50.00
	weight = float(visibility * position * freshness * visittime * visitfrequency)/5.00
	User_Matrix[1][1] = weight
	for j in range(2,num_lines+1):
		visibility = float(0)/3.00
		position = float(0)/2.00
		freshness = float(0)/10.00
		visittime = float(0)/600.00
		visitfrequency = float(0)/50.00
		weight = float(visibility * position * freshness * visittime * visitfrequency)/5.00
		User_Matrix[1][j] = weight
	for i in range(2,5):
		for j in range(1,num_lines+1):
			visibility = float(documents[metaurl[j - 1]].visibility/documents[metaurl[j - 1]].count)/3.00
			position = float(documents[metaurl[j - 1]].position/documents[metaurl[j - 1]].count)/2.00
			freshness = float(random.randint(1, 10))/10.00
			visittime = float(random.randint(1, 600))/600.00
			visitfrequency = float(random.randint(1, 50))/50.00
			weight = float(visibility * position * freshness * visittime * visitfrequency)/5.00
			User_Matrix[i][j] = weight

	print User_Matrix

	for i in range(2,5):
		dataSetI = (User_Matrix[1][1:])
		dataSetII = User_Matrix[i][1:]
		result = 1 - spatial.distance.cosine(map(float,dataSetI), map(float,dataSetII))
		print result
		if(result > 0.0075):
			print User_Matrix[i]
			for j in range(1,num_lines+1):
				if(User_Matrix[i][j]>0.0050):
					print User_Matrix[0][j]
			print('\n')

def showUsage():
    print("rank usage:")
    print("   rank inputFilemeta inputpagerank")
    print("Examples:")
    print("  python user-pagematrix.py meta.txt pagerank.dump ")

def main():
    if (len(sys.argv) < 2):
        showUsage()
    else:
        inputFileName1 = sys.argv[1]
        inputFileName2 = sys.argv[2]
        documents = {}
        processDocuments(documents,inputFileName2)
        usermat(inputFileName1,documents)
        print("done!")

main()