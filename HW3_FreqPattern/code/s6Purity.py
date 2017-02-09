# Step 6: Re-rank by Purity of Patterns (10pts)
# A phrase is pure in topic t if it is only frequent in documents 
# ( here documents refer to titles) about topic t and not frequent in documents about other topics. 
# For example, 'query processing' is a more pure phrase than 'query' in the Database topic. 
# We measure the purity of a pattern by comparing the probability of seeing a phrase 
# in the topic-t collection D(t) and the probability of seeing it in any other topic-t' collection.
# In our case, k=4. The definition is as follows:
# purity(p,t)=log [ f(t,p) / | D(t) | ] - log (max [ ( f(t,p) + f(t',p) ) / | D(t,t') | ] )
# Here, log base is 2. f(t,p) is the frequency of pattern p appearing in topic t 
# (i.e., support of p in topic-t.txt). We define D(t) to be the collection of documents 
# where there is at least one word being assigned the topic t. 
# D(t) = { d | topic t is assigned to at least one word in d }
# and D(t,t') is the union of D(t) and D(t'). 
# Actually | D(t) | is exactly the number of lines in topic-i.txt. 
# But note that | D(t,t') | != | D(t) | + | D(t') |.
# Re-rank the patterns obtained from Step 4. The output should be of the form:
# Purity         [frequent pattern] 
# Purity         [frequent pattern] 
# ...
# and frequent patterns are sorted from high to lowby a measure which combines Support and Purity 
# (you will need to come up with how to combine them). 
# Your output files should be put into one directory named as purity. 

# take patterns/pattern-i.txt as arguments, and output purity/purity-i.txt

import math
import pandas as pd

def getSup(file,pat):
	cnt = 0
	for line in file:
		words = line.strip().split()
		if set(pat).issubset(words):
			cnt += 1
	return cnt

def purity():
	output = [open('purity/purity-{}.txt'.format(i),'w') for i in range(5)]
	for t in range(5):
		ret = []
		allFile = [open('topic-{}.txt'.format(i),'r') for i in range(5)]
		fin = []
		for i in range(5):
			fin.append(allFile[i].readlines())
			allFile[i].close()

		# get all the union size
		sizes = {}
		for i in range(5):
			for j in range(i+1,5):
				# uniform every pattern as set in order to compare
				pati = [tuple(sorted(p.strip().split())) for p in fin[i]]
				patj = [tuple(sorted(p.strip().split())) for p in fin[j]]
				union = set(pati+patj)
				sizes[tuple([i,j])] = len(set(union))

		with open('patterns/pattern-{}.txt'.format(t),'r') as curFile:
			curFile = curFile.readlines()
			for line in curFile:
				# get freq pattern
				pat = tuple(line.split()[1:])

				# get sup in all files
				sup = []
				for i in range(5):
					sup.append(getSup(fin[i],pat))

				# compute purity
				purity = []
				localSup = sup[t]
				localD = len(fin[t])
				for j in range(5):
					if j!= t:
						otherSup = sup[j]
						unionD = sizes[tuple(sorted([j,t]))]
						curPurity = math.log(localSup/float(localD),2) - math.log((localSup+otherSup)/float(unionD),2)
						purity.append(curPurity)

				# select the minmum and assign to this pattern

				ret.append(tuple([pat,min(purity),localSup/float(localD)]))

		df = pd.DataFrame(ret,columns=['pat','purity','sup'])
		sort_df = df.sort_values(['purity','sup'],ascending=[0, 0])
		sortMat = sort_df.as_matrix()
		for line in sortMat:
			output[t].write('{0:.4f} '.format(line[1])+' '.join(line[0])+'\n')

		output[t].close()


if __name__ == '__main__':
	purity()