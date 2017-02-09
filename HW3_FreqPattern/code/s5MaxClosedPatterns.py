# Step 5: Mining Maximal/Closed Patterns (20pts)
# In this step, you need to implement an algorithm to mine maximal patterns and closed patterns. 
# You could write the code based on the output of Step 4, or implement a specific algorithm to mine maximal/closed patterns, 
# such as CLOSET, MaxMiner, etc.
# The output should be of the same form as the output of Step 4. 
# Max patterns are put into max directory. The i-th file is named as max-i.txt.
# Closed patterns are put into closed directory. The i-th file is named as closed-i.txt.

from s4MiningFreqPatterns import *

def MiningMaxPat(min_sup):
    inputFile = [open('patterns/pattern-{}.txt'.format(i),'r') for i in range(5)]
    output = [open('max/max-{}.txt'.format(i),'w') for i in range(5)]
    for t in range(5):
        inputLines = inputFile[t].readlines()
        sup_pat = dict()
        # put the freq pat and their sup into a dictionary
        for line in inputLines:
        	sup = line.split()[0]
        	pat = tuple(line.split()[1:])
        	sup_pat[pat] = int(sup)

        # iterate all dict to find max pat
        for pat1 in sup_pat.keys():
        	for pat2 in sup_pat.keys():
        		if set(pat1).issubset(set(pat2)) and pat1 != pat2:
        			del sup_pat[pat1]
        			break

        # sort the support and write to output files
        sortKey = sorted(sup_pat,key=sup_pat.get,reverse=True)
        for key in sortKey:
            if isinstance(key,tuple):
                output[t].write(str(sup_pat[key])+' '+' '.join(key)+'\n')
            else:
                output[t].write(str(sup_pat[key])+' '+key+'\n')
        inputFile[t].close()
        output[t].close()
    
def MiningClosedPat(min_sup):
    inputFile = [open('patterns/pattern-{}.txt'.format(i),'r') for i in range(5)]
    output = [open('closed/closed-{}.txt'.format(i),'w') for i in range(5)]
    for t in range(5):
        inputLines = inputFile[t].readlines()
        sup_pat = dict()
        # put the freq pat and their sup into a dictionary
        for line in inputLines:
        	sup = line.split()[0]
        	pat = tuple(line.split()[1:])
        	sup_pat[pat] = int(sup)

        # iterate all dict to find closed pat
        for pat1 in sup_pat.keys():
        	for pat2 in sup_pat.keys():
        		if set(pat1).issubset(set(pat2)) and pat1 != pat2 and sup_pat[pat1]==sup_pat[pat2]:
        			del sup_pat[pat1]
        			break

        # sort the support and write to output files
        sortKey = sorted(sup_pat,key=sup_pat.get,reverse=True)
        for key in sortKey:
            if isinstance(key,tuple):
                output[t].write(str(sup_pat[key])+' '+' '.join(key)+'\n')
            else:
                output[t].write(str(sup_pat[key])+' '+key+'\n')
        inputFile[t].close()
        output[t].close()
    
if __name__ == '__main__':
	MiningMaxPat(0.01)
	MiningClosedPat(0.01)

