#!/usr/bin/python
import sys
import urllib2
from bs4 import BeautifulSoup
import re

mediafile = re.compile(r".*\.(jpg|png|gif|pdf|mp4|flv|mp3|webm|avi)$")

def explore(url, depth, stop, documents, outbound, problems,visibility,position,descriptions,keywords):
    if (url not in documents and depth < stop and not mediafile.match(url)):
        print("adding = " + url + ", documents size = " + str(len(documents)))
        documents.append(url)
        outbound.append([])
        visibility.append([])
        position.append([])
        boldocument = {}
        italicdocument = {}
        fullUrl =  url
        
        #User-Agent must be set because wikipedia blocks crawlers
        request = urllib2.Request(fullUrl)
        try:
            socket  = urllib2.urlopen(request)
            page    = socket.read()
            socket.close()
            
            soup = BeautifulSoup(page,"lxml")
            index = documents.index(fullUrl)
            destag = soup.find("meta", {"name":"description"})
            if (destag):
            	descriptions.append(destag.get("content"))
            else:
            	descriptions.append("")

            keytag = soup.find("meta", {"name":"keywords"})
            if (keytag):
            	# print keytag.get("content")
            	keywords.append(keytag.get("content"))
            else:
            	keywords.append("")
            	#print key['content'].encode('utf-8')
                #if(key.get('content-length')):
            	 #  keywords[index] = key['content'].encode('utf-8')
            #print(keywordss)
            #print(descriptions)
            if soup:
            	for boldtag in soup.find_all("b"):
            		for boldlink in boldtag.find_all("a"):
            			boldocument[boldlink.get("href")] = boldlink
                for italictag in soup.find_all("i"):
                    for italiclink in italictag.find_all("a"):
                        italicdocument[italiclink.get("href")] = italiclink
            	alllinks = soup.find_all('a',href = True)
            	#print(alllinks)
            	totallinks = len(alllinks)
                for count,link in enumerate(alllinks):
                    # print fullUrl
                    if (link.get("href") not in documents):
                    	visibility[index].append(1)
                    	if (link.get("href") in boldocument):
							visibility[index][-1] = 3
                        elif(link.get("href") in italicdocument):
                            visibility[index][-1] = 2
                        if(count < (totallinks/2)):
							position[index].append(2)
                        else:
							position[index].append(1)
                        if (link.get("href") and link.get("href")[0] == "/"):
                        	initiallink = fullUrl[:fullUrl[8:].find("/")+8]
                        	explore(initiallink+link.get("href"), depth + 1, stop, documents, outbound, problems, visibility,position,descriptions,keywords)
                        	outbound[index].append(initiallink+link.get("href"))
                        elif(link.get("href") and link.get("href")[0] == "h"):
                        	explore(link.get("href"), depth + 1, stop, documents, outbound, problems, visibility,position,descriptions,keywords)
                        	outbound[index].append(link.get("href"))
			
            else:
                documents.pop()
                outbound.pop()
                visibility.pop()
                position.pop()
                problems.append(url)

        except IOError, (errno):
            print "HUGE ERROR MOVING ON"
            documents.pop()
            outbound.pop()
            visibility.pop()
            position.pop()

#accpets a list of documents and a corresponding list of lists of
#outbound urls, writes the adjacency list to the specified outFile
def dumpLists(documents, outbound, outFile, outFile2, visibility,position,descriptions,keywords): #avani
    f = open(outFile, "w")
    for index, url in enumerate(documents):
        f.write(url + ":\n") #avani
        boldlink = visibility[index]
        posvalue = position[index]
        for count, link in enumerate(outbound[index]):
            f.write("   " + link + "   " + str(posvalue[count]) + "   " + str(boldlink[count]) + "\n") #avani
    f = open(outFile2, "w")
    for index, url in enumerate(documents):
    	f. write(url + ":" + keywords[index] + "\n" )


#accepts a list of urls and writes them to sdtout
def dumpProblems(problems):
    print("Problems")
    for url in problems:
        print("   " + url)

#prints usage information for crawl
def showUsage():
    print("Crawl Usage:")
    print("   crawl targetUrl searchDepth outFile outfile2")
    print("Examples:")
    print("  python crawl.py 3 pagerank.dump meta.dump")
    print("  python crawl.py 5 pagerank.dump meta.dump")

def main():
    if (len(sys.argv) < 4):
        showUsage()
    else:
        url = 'http://www.yellowpages.co.in/'
        stop = int(sys.argv[1])
        outFile = sys.argv[2]
        outFile2 = sys.argv[3]
        documents = []
        outbound = []
        problems = []
        vis = []
        position = []
        descriptions = []
        keywords = []
        explore(url, 0, stop, documents, outbound, problems, vis, position,descriptions,keywords) #avani
        dumpLists(documents, outbound, outFile, outFile2, vis, position,descriptions,keywords)
        #dumpProblems(problems)

main()
