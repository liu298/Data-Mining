# Step 4: Mining Frequent Patterns for Each Topic (30pts)
# In this step, you need to implement a frequent pattern mining algorithm. 
# You can choose whatever frequent pattern mining algorithms you like, such as Apriori, FP-Growth, ECLAT, etc. 
# Note that you need to run your code on 5 files corresponding to 5 topics. 
# The output should be of the form ( [s] (space) [t1 (space) t2 (space) t3 (space) ...] ), 
# where each term should be represented as the term id:
# #Support          [frequent pattern] 
# #Support          [frequent pattern] 
# ...
 
# and frequent patterns are sorted from high to low by #Support. 
# Your output files should be put into one directory named as patterns. The i-th file is named as pattern-i.txt.

import os

def ChooseCand(prePat,n):
    """
    :type prePat: list of tuples
    :rtype: list of tuples
    
    """
    ret = []
    prePat = sorted(prePat)
    for i in range(len(prePat)):
        # join step
        cur = prePat[i]
        ## find intersections in pattern behind
        for j in range(i+1,len(prePat)):
            after = prePat[j]
            if(isinstance(prePat[0],tuple)):
                intersec = set(filter(lambda x: x in cur,after))
                if len(intersec)==n-2:
                    ## possible to grenerate a new candidate
                    new = set(sorted(cur+after))
                    # prune step
                    if not hasInfreq(new,prePat) and tuple(new) not in ret:
                        ret += [tuple(new)]
            else:
                ret += [(cur,after)]
    return ret

def hasInfreq(items,prePat):
    for i in items:
        sub = items-set(i)
        if tuple(sub) not in prePat:
            return True
    return False

def AprioriMining(file,n,min_sup):
    """
    :rtype: list
    """
    ret = {}
    if n == 1: # base case
        patCount = {}
        lineCount = 0
        for line in file:
            lineCount += 1
            words = line.split()
            for word in words:
                if word not in patCount:
                    patCount[word]=1
                else:
                    patCount[word]+=1
        for key,val in patCount.items():
        	if val/(lineCount+0.0) >= min_sup:
        		ret[key] = val
    else:
        if n> 1:
            prePat = AprioriMining(file,n-1,min_sup).keys()
            if len(prePat)!=0:
                candids = ChooseCand(prePat,n)
                patCount = dict(zip(candids,[0]*len(candids)))
                lineCount = 0
                for line in file:
                    lineCount += 1
                    words = set(line.split())
                    for candid in candids:
                        if set(candid).issubset(words):
                            patCount[candid] += 1
                for key,val in patCount.items():
                    if val/(lineCount+0.0) >= min_sup:
                        ret[key] = val
    return ret


# def test():
#     with open('topic-0.txt','r') as file:
#         file = file.readlines()
#         print(AprioriMining(file,1,0.01))

# if __name__ == '__main__':
# 	test()

def MiningAllPat(min_sup):
	inputFile = [open('topic-{}.txt'.format(i),'r') for i in range(5)]
	# os.makedirs('patterns')
	output = [open('patterns/pattern-{}.txt'.format(i),'w') for i in range(5)]

	for t in range(5):
		ret = dict()
		inputLines = inputFile[t].readlines()
		for i in range(9999):
			fp = AprioriMining(inputLines,i+1,min_sup)
			ret.update(fp)
	    # print(str(i+1),len(ret))
			if len(fp)==0:
				break
		# sort the support
		sortKey = sorted(ret,key=ret.get,reverse=True)

		# write to output files with '#sup pat pat' each line
		for key in sortKey:
			if isinstance(key,tuple):
				output[t].write(str(ret[key])+' '+' '.join(key)+'\n')
			else:
				output[t].write(str(ret[key])+' '+key+'\n')
		inputFile[t].close()
		output[t].close()
    
if __name__ == '__main__':
	MiningAllPat(0.01)
