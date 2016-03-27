################################################################
#findEvalBestPeARS.py
################################################################

from utils import cosine_similarity
import numpy as np
from math import isnan

num_best_pears=5



###################################################
#Sort scores and output n best pears
###################################################

def outputBestPears(pears_scores):
	#print "Outputting best pears..."
	pears=[]
	c=0
	for w in sorted(pears_scores, key=pears_scores.get, reverse=True):
		if c < num_best_pears:
			#print w, pears_scores[w]
			pears.append(w)
			c+=1
		else:
			break
	return pears


#############################################
#Main function, called by mkQueryPage.py
##############################################

def runScript(query_dist,dm_dict,pears_ids):
	best_pears=[]
		
	#############################################################
	#Calculate score for each pear in relation to the user query
	#############################################################

	if len(query_dist) > 0:	
		pears_scores={}
		for pear_name,v in pears_ids.items():
			scoreSIM = 0.0		#Initialise score for similarity
			score=cosine_similarity(np.array(v),query_dist)
			if not isnan(score):
				pears_scores[pear_name]=score
				print pear_name,score	
		best_pears=outputBestPears(pears_scores)
	return best_pears
