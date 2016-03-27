################################################################
# utils includes all the utility methods being used throughout
# the codebase
################################################################



from numpy import *
import re
import time

stopwords=["","(",")","a","about","an","and","are","around","as","at","away","be","become","became","been","being","by","did","do","does","during","each","for","from","get","have","has","had","her","his","how","i","if","in","is","it","its","made","make","many","most","of","on","or","s","some","that","the","their","there","this","these","those","to","under","was","were","what","when","where","who","will","with","you","your"]

num_dim=400

########################################################
# Normalise array
########################################################

def normalise(v):
    norm=linalg.norm(v)
    if norm==0: 
       return v
    return v/norm

#############################################
# Cosine function
#############################################

def cosine_similarity(peer_v, query_v):
    if len(peer_v) != len(query_v):
        print len(peer_v),len(query_v)
        raise ValueError("Peer vector and query vector must be "
                         " of same length")
    num = dot(peer_v, query_v)
    den_a = dot(peer_v, peer_v)
    den_b = dot(query_v, query_v)
    return num / (sqrt(den_a) * sqrt(den_b))

######################################################
# Make distribution for query with entropy weighting
######################################################

def mkQueryDistEntropy(query,dm_dict,entropies):
    words = query.rstrip('\n').split('+')
    # Only retain arguments which are in the distributional semantic space
    vecs_to_add = []
    for w in words:
	w=w.lower()									#CBOW model is all uncapitalised
	w=w.replace(',','')
	w=w.replace('\"','')
 	if w not in stopwords:
		if w in dm_dict:
			#print "Adding word",w
			vecs_to_add.append(w)
		else:
			print "UNKNOWN WORD:",w

    vbase = array([])
    # Add vectors together
    if len(vecs_to_add) > 0:
        # Take first word in vecs_to_add to start addition
        vbase = array(dm_dict[vecs_to_add[0]])
	vbase=zeros(num_dim)
        for w in vecs_to_add:
		if w in entropies:
			if math.log(entropies[w]+1) > 0:
				weight=float(1)/float(math.log(entropies[w]+1))
				#print w,weight
				vbase = vbase+weight*array(dm_dict[w])
    vbase=normalise(vbase)
    return vbase



# Timing function, just to know how long things take


def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s in scorePages took %0.3f ms' % (func.func_name, (t2 - t1) * 1000.0)
        return res
    return wrapper


