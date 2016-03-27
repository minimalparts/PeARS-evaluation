########################################################################
# getUrlOverlap.py takes a (raw, non-lemmatised) query and a URL and 
# calculates the dice coefficient between the two strings (jaccard also 
# available). Higher scores represent higher match between query and url.
# To be integrated as a module in final search algorithm
# USAGE: python ./getUrlOverlap.py  wikipedia https://en.wikipedia.org/
########################################################################


import sys
import re

stopwords=["","(",")","a","about","an","and","are","around","as","at","away","be","become","became","been","being","by","did","do","does","during","each","for","from","get","have","has","had","he","her","his","how","i","if","in","is","it","its","made","make","many","most","not","of","on","or","s","she","some","that","the","their","there","this","these","those","to","under","was","were","what","when","where","which","who","will","with","you","your"]

def jaccard(a, b):
	c = a.intersection(b)
	return float(len(c)) / (len(a) + len(b) - len(c))

def dice(a, b):
	c = a.intersection(b)
	return float(2*len(c)) / (len(a) + len(b))

def completeWordOverlap(query, url):
	score=0
	q_length=0
	words=query.split('+')
	for w in words:
		#if w in b or w[:-1] in b:		#w[:-1] is a hack to deal with plurals in query
		if w not in stopwords: 
			q_length+=1
			if w in url.split('_'):
				score+=1
	if q_length > 0:
		return float(score)/float(q_length)
	else:
		return 0


def wikipediaWordOverlap(query,url):
        score=0
	q_words=query.split('+')
        m=re.search(".*/(.+)",url)
        if m:
                url=m.group(1)
        u_words=re.split('\W+|_', url)
	for w in u_words:
		w=w.replace(',','')
		if w not in stopwords and w in q_words:
			score+=1
	return float(score)/float(len(u_words))


def scoreUrlOverlap(query,url):
	url=url.rstrip('/')		#Strip last backslash if there is one
	m=re.search('.*/([^/]+)',url)	#Get last element in url
	if m:
		url=m.group(1)
	
	#print jaccard(set(query.lower()), set(url.lower()))
	#print dice(set(query.lower()), set(url.lower()))
	#return completeWordOverlap(query.lower(),url.lower())
	return wikipediaWordOverlap(query.lower(),url.lower())
	


def runScript(query,url):
	#print scoreUrlOverlap(query,url)
	return scoreUrlOverlap(query,url)

# when executing as script
if __name__ == '__main__':
    runScript(sys.argv[1],sys.argv[2])      #Input query,url

