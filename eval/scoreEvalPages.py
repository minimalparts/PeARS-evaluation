#######################################################################
# Use with name of pear and query
####################################################################### 

import getUrlOverlap
from utils import cosine_similarity

#Change this line to your PeARS folder path
path_to_PeARS="/home/user/PeARS-evaluation/"


###############################################
# Get distributional score
###############################################

def scoreDS(query_dist,url_dict):
    DS_scores={}
    for url,doc_dist in url_dict.items():
    	score = cosine_similarity(doc_dist, query_dist)
    	DS_scores[url] = score
    return DS_scores


###############################################
# Get url overlap score
###############################################

def scoreURL(query,url_dict):
    URL_scores={}
    for u in url_dict:
        URL_scores[u]=getUrlOverlap.runScript(query,u)
        #print v,"URL score",URL_scores[v]
    return URL_scores


################################################
# Score documents for a pear
################################################

def scoreDocs(query, query_dist, url_dict):
    doc_scores = {}  # Document scores
    DS_scores=scoreDS(query_dist,url_dict)
    URL_scores=scoreURL(query,url_dict)
    for v in url_dict:
        if v in DS_scores and v in URL_scores:
                if URL_scores[v] > 0.7 and DS_scores[v] > 0.2:                                      #If URL overlap high (0.2 because of averag e length of query=4 -- see getUrlOverlap --  and similarity okay
                        doc_scores[v]=DS_scores[v]+URL_scores[v]*0.2                                #Boost DS score by a maximum of 0.2
                else:
                	doc_scores[v]=DS_scores[v]
	if math.isnan(doc_scores[v]):								    #Check for potential NaN -- messes up with sorting in bestURLs.
		doc_scores[v]=0
    return doc_scores	

#################################################
# Get best URLs
#################################################

def bestURLs(url_scores):
	best_urls={}
	for w in sorted(url_scores, key=url_scores.get, reverse=True):
		if url_scores[w] > 0.3:					#Threshold - page must be good enough
			best_urls[w]=url_scores[w]
	return best_urls


################################################
# Prepare output
################################################


def output(best_urls):
	results=[]
#	print query	
	#If documents matching the query were found on the pear network...
	if len(best_urls) > 0:
		for u in best_urls:
			results.append(u)			

	#Otherwise, open duckduckgo and send the query there
	else:
		print "No suitable pages found."
		results.append("")
	return results

##############################################
#Main function - score pages for one pear
##############################################

def runScript(query_dist,url_dict):
	#document_scores=scoreDocs(query, query_dist, url_dict):	#with URL overlap
	document_scores=scoreDS(query_dist, url_dict)			#without URL overlap
	best_urls=bestURLs(document_scores)
	return best_urls

