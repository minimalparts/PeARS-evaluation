import sys
import re

user_pages={}

def printUsers():
	for u,p in user_pages.items():
		pages=""
		for page in p:
			pages+=page.replace(' ','_')+" "
		pages=pages[:-1]
		print u.replace(' ','_')+"::"+str(len(p))+"::"+pages

def loadUserLog(log_file):
	log=open(log_file,'r')
	logitem=[None,None]
	record_log=True
	for l in log:
		l=l.rstrip('\n')
		if "</logitem>" in l:
			for i in range(len(logitem)):
				if logitem[i] is None:
					record_log=False
					break
			if record_log:
				if logitem[0] in user_pages:
					if logitem[1] not in user_pages[logitem[0]]:
						user_pages[logitem[0]].append(logitem[1])
				else:
					user_pages[logitem[0]]=[logitem[1]]
		
					
			logitem=[None,None]
			record_log=True
		if "<username>" in l:
			m=re.search("<username>(.*)</username>",l)
			if m:
				logitem[0]=m.group(1)
		if "<logtitle>" in l:
			m=re.search("<logtitle>(.*)</logtitle>",l)
			if m:
				title=m.group(1)
				special_doc=False
				specials=["File:","User:","Template:","MediaWiki:","Wikipedia:","Talk:","Category:"]
				for w in specials:
					if w in title:
						special_doc=True
				if not special_doc:
					logitem[1]=title
				
	log.close()

loadUserLog(sys.argv[1])
printUsers()
