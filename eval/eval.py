import sys
import re
import time
import numpy as np
import findEvalBestPears, scoreEvalPages
from utils import mkQueryDistEntropy,cosine_similarity,normalise

path_to_PeARS="/home/user/PeARS-evaluation/"
shared_pears_ids=path_to_PeARS+"eval/shared_pears_ids.dm"
path_to_nodes=path_to_PeARS+"DS/user-pears/"
score=0

#################################################
# Read dm file
#################################################

def readDM():
	print "Loading dm space..."
	dm_dict={}
	with open("../DS/ukwac.predict.dm") as f:
		dmlines=f.readlines()
		f.close()

	#Make dictionary with key=row, value=vector
	for l in dmlines:
		items=l.rstrip('\n').split('\t')
		row=items[0]
		vec=[float(i) for i in items[1:]]
		dm_dict[row]=normalise(vec)
	print "Space loaded..."
	return dm_dict


##############################################
# Read pears  ids
##############################################

def readPears():
	pears_ids={}
	sp=open(shared_pears_ids,'r')
	for l in sp:
		l=l.rstrip('\n')
		items=l.split()
		pear_name =  items[0]
		pear_dist =[float(i) for i in items[1:]]
		pears_ids[pear_name]=pear_dist
	sp.close()
	return pears_ids

#################################################
# Load entropy list
#################################################

def loadEntropies():
	entropies_dict={}
	f=open("../DS/ukwac.entropy.txt","r")
	for l in f:
		l=l.rstrip('\n')
		fields=l.split('\t')
		w=fields[0].lower()
		if w.isalpha() and w not in entropies_dict:			#Must have this cos lower() can match two instances of the same word in the list
			entropies_dict[w]=float(fields[1])
	f.close()
	return entropies_dict

##############################################
# Get URL-vector dict
#############################################

def getUrlDict(pear):
    url_dict={}
    doc_dists = open(path_to_nodes+pear+".urls.dists.txt")
    for l in doc_dists:
        l = l.rstrip('\n')
	fields=l.split()
        url = fields[0]
	m=re.search(".*/(.*)",url)
	if m:
		title=m.group(1).lower()
	doc_dist =[float(i) for i in fields[1:]]
	url_dict[title]=doc_dist
    doc_dists.close()
    #print pear,"(",len(url_dict),"pages)",
    return url_dict

#############################################
# Write query dist
#############################################

def writeQueryDM(query_dists):
	f=open("queries.add.dm",'w')
	for q,d in query_dists.items():
		dist_str=""
		for n in d:
			dist_str=dist_str+"%.6f" % n+" "
		dist_str=dist_str[:-1]
		f.write(q+"::"+dist_str+'\n')
	f.close()		

#############################################
# Start of script
#############################################

dm_dict=readDM()
pears_ids=readPears()
entropies_dict=loadEntropies()
query_dists={}
results={}

pear_score=0
page_score=0
rank_sum=0

counter=0


start_search=time.time()

num_queries=0
wf=open(sys.argv[1],'r')
for l in wf:
	results.clear()
	l=l.rstrip('\n')
	items=l.split("::")
	query=re.sub(" |\'|\!|\?","+",items[0])
	query=re.sub("\+$","",query)
	answer=items[1].lower().replace(' ','_')
	print "*****"
	print "Processing query:",query,"(answer:",answer,")"
	print "*****"
	query_dist=mkQueryDistEntropy(query,dm_dict,entropies_dict)
	query_dists[query]=query_dist
	#start_pear_search=time.time()
	pears=findEvalBestPears.runScript(query_dist,dm_dict,pears_ids)
	#print "TIME FOR PEAR SEARCH",time.time()-start_pear_search,"s."
	num_pages_inspected=0
	answer_pears=[]			
	if len(pears) > 0:
		ps=0
		for pear in pears:
			url_dict=getUrlDict(pear)
			num_pages_inspected+=len(url_dict)
			if answer in url_dict:
				ps=1
			pair=[pear,str(len(url_dict))]
			answer_pears.append(pair)
			#start_page_search=time.time()
			pear_results=scoreEvalPages.runScript(query_dist,url_dict)
			#print "TIME FOR PAGE SEARCH",time.time()-start_page_search,"s."
			for k,v in pear_results.items():
				results[k]=v
		print ""
		if ps==1:
			pear_score+=1
		
		c=0
		score=0
		rank=0
		for w in sorted(results, key=results.get, reverse=True):
			if c<20:
				print w,results[w]
				if w == answer:
					page_score+=1
					score=1
					rank=c+1
					#print "PAGE SCORE +1"
				c+=1
		counter+=1
		print "NUMBER OF PAGES INSPECTED:",num_pages_inspected,"PEAR SCORE:",ps,"PAGE SCORE:",score,"RANK:",rank
		#if ps > 0:
		#	print "ANSWER PEARS",answer_pears
		print "SELECTED PEARS",answer_pears
		print "CURRENT PAGE SCORE",float(page_score)/float(counter)
		print "CURRENT PEAR SCORE",float(pear_score)/float(counter)
		if rank == 0:
			inv_rank=0
		else:
			inv_rank=1.0/float(rank)
		rank_sum+=inv_rank
		print "CURRENT RANK SCORE",float(rank_sum)/float(counter)
		
	else:
		print "SORRY, NO GOOD PEAR FOUND."
	num_queries+=1
wf.close()

print "OVERALL PAGE SCORE",float(page_score)/float(counter)
print "OVERALL PEAR SCORE",float(pear_score)/float(counter)

end_search=time.time()
print "\nOVERALL TIME",end_search-start_search,"s."
print "TIME PER QUERY",float(end_search-start_search)/float(num_queries),"s."
writeQueryDM(query_dists)
