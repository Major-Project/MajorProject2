#!/usr/bin/python

import sys
import time
import re
import urllib2
import random
from sys import stdout
from math import sqrt
from math import pow
from bs4 import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

metasimilarity = {}

def metasimilar(documents, inputFileName):
    print("reading from input files...")
    inputFile = open(inputFileName, "r")
    data = inputFile.read()
    metadata = re.findall(".".join(["[^.]+"] * 4), data)
    first_line = metadata[0][metadata[0].find(":",6)+1:]
    #print first_line
    keywords1 = first_line.split(",")
    #print keywords1
    i=1
    count = 0
    metasimilaritypage = 0
    inputFile = open(inputFileName, "r")
    inputFile.next()
    for line in inputFile:
        print line
        if line.find(":",6):
            for word1 in keywords1:
                for word2 in metadata[i][metadata[i].find(":",6)+1:].split(","):
                    keyword1 = word1.strip().replace(" ","+")
                    print keyword1
                    keyword2 = word2.strip().replace(" ","+")
                    print keyword2
                    
                    url1 = ('https://www.bing.com/search?q=%s' % keyword1)
                    url2 = ('https://www.bing.com/search?q=%s' % keyword2)
                    url  = ('https://www.bing.com/search?q=%s+%s' %(keyword1, keyword2))
                    print url
                    request1 = urllib2.Request(url1, headers = hdr)
                    request2 = urllib2.Request(url2, headers = hdr)
                    request = urllib2.Request(url, headers = hdr)
                    try:
                    	time.sleep(random.randint(3,5))
                        socket  = urllib2.urlopen(request1, None, 120)
                        page    = socket.read()
                        socket.close()
                        soup1 = BeautifulSoup(page,"lxml")

                        time.sleep(random.randint(3,5))
                        socket  = urllib2.urlopen(request2, None, 120)
                        page    = socket.read()
                        socket.close()
                        soup2 = BeautifulSoup(page,"lxml")
                        
                        time.sleep(random.randint(3,5))
                        socket  = urllib2.urlopen(request, None, 120)
                        page    = socket.read()
                        socket.close()
                        soup = BeautifulSoup(page,"lxml")
                        
                        resultStat1 = soup1.find("span", {"class":"sb_count"})
                        resultStat2 = soup2.find("span", {"class":"sb_count"})
                        resultStat = soup.find("span", {"class":"sb_count"})
                        if(resultStat and resultStat1 and resultStat2):
                        	pagecount1 = float(resultStat1.text.split()[0].replace(",",""))
                        	print url1
                        	print pagecount1
                        	pagecount2 = float(resultStat2.text.split()[0].replace(",",""))
                        	print url2
                        	print pagecount2
                        	pagecount = float(resultStat.text.split()[0].replace(",",""))
                        	print url
                        	print pagecount
                        	metasimeachword = float(pagecount/(pagecount1 + pagecount2 - pagecount))
                        	metasimilaritypage = float(metasimilaritypage + metasimeachword)
                        	count = count + 1;

                        

                    except IOError, (errno):
                        print errno
            metasimilarity[line] = float(metasimilaritypage/count)
            print metasimilarity[line]
            print metasimilarity

            i = i+1

        #else:
            #continue

def printMeta(outputFileName):
    print("writing to output file...")
    outputFile = open(outputFileName, "w")
    for url in metasimilarity:
        if(metasimilarity[url] > 0.001):
            outputFile.write(url + ":" + str(metasimilarity[url]) + "\t" + "\n")

def showUsage():
    print("meta usage:")
    print("   meta inputFile outputFile")
    print("Examples:")
    print("  python meta.py meta.dump meta.txt") 

def main():
    if (len(sys.argv) < 2):
        showUsage()
    else:
        inputFileName = sys.argv[1]
        outputFileName = sys.argv[2]
        documents = {}
        metasimilar(documents, inputFileName)
        printMeta(outputFileName)
        print("done!")

main()
