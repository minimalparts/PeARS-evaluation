####################################################################
# Make pears for specific users using a list of documents they have
# read.
# USAGE: python ./mkpears.py usernames.txt users.pages.edited.txt
####################################################################

import sys
import re

dists={}
userpages={}

def readDM():
	f=open("example.docs.dm")
	for l in f:
		l=l.rstrip('\n')
		fields=l.split()
		m=re.search("/([^/]+)$",fields[0])
		if m:
			page=m.group(1)
		dists[page]=l
	f.close()

def readUsers(usernames_file):
	users=[]
	f=open(usernames_file,'r')
	for l in f:
		l=l.rstrip('\n')
		users.append(l)
	f.close()
	return users

def readEditedPages(pages_edited_file):
	f=open(pages_edited_file,'r')
	for l in f:
		l=l.rstrip('\n')
		fields=l.split("::")
		user=fields[0]
		pages=fields[2].split()
		userpages[user]=pages
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
def runScript(usernames_file,pages_edited_file):
	users=readUsers(usernames_file)
	print "Found",len(users),"users..."
	readEditedPages(pages_edited_file)
	readDM()

	for u in users:
		pages=userpages[u]
		if len(pages)>0:
			print u
			getDists(pages,u)

# when executing as script
if __name__ == '__main__':
    runScript(sys.argv[1],sys.argv[2])	
