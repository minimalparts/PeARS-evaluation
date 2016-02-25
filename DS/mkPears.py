####################################################################
# Make pears for specific users using a list of documents they have
# read.
####################################################################

import sys
import re

dists={}
userpages={}

def readDM():
	f=open("wikiQA.1242.urls.dists.dm")
	for l in f:
		l=l.rstrip('\n')
		fields=l.split()
		m=re.search("/([^/]+)$",fields[0])
		if m:
			page=m.group(1)
		dists[page]=l
	f.close()

def readUsers():
	users=[]
	f=open("../wiki-users/wikiQA.1242.usernames.txt",'r')
	#f=open("usernames.tmp",'r')
	c=0
	for l in f:
		if c > 0:
			l=l.rstrip('\n')
			users.append(l)
		else:
			c+=1
	f.close()
	return users

def readEditedPages():
	f=open("../wiki-users/wikiQA.1242.users.pages.edited.txt",'r')
	c=0
	for l in f:
		if c > 0:						#Don't read first line
			l=l.rstrip('\n')
			fields=l.split('\t')
			m=re.search(" (.*)",fields[0])
			if m:
				user=m.group(1)
				pages=fields[1:]
				userpages[user]=pages
		else:
			c+=1
	return pages

def getDists(pages,user):
	pear="user-pears/"+user+".urls.dists.txt"
	out_pear=open(pear,'w')
	for page in pages:
		if page in dists:
			out_pear.write(dists[page]+"\n")
	out_pear.close()

##################################
# Entry point
##################################

users=readUsers()
print "Found",len(users),"users..."
readEditedPages()
readDM()


for u in users:
	pages=userpages[u]
	if len(pages)>0:
		print u
		getDists(pages,u)
