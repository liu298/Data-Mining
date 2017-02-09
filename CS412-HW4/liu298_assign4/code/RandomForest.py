# Step 3: Implement Ensemble Classification Method

import sys
from DecisionTree import *
import random
import math



def randomAttrCand(data):
	candidates = []
	num_attr = len(data[0])-1
	n= int(math.sqrt(num_attr))
	attrs = random.sample(range(1,num_attr+1),n)
	for row in data:
		if isinstance(attrs, int):
			i = attrs
			if (i,row[i]) not in candidates:
				candidates.append((i,row[i]))
		else: 
			for i in attrs:
				if (i,row[i]) not in candidates:
					candidates.append((i,row[i]))
	return candidates

def bootstrapData(data):
	sample = []
	for i in range(len(data)):
		idx = random.randrange(len(data))
		sample.append(data[idx])
	return sample
	
def BuildRandomForest(data,nTrees,entroFunc,splitCandFun):
	forest = []
	for i in range(nTrees):
		sample = bootstrapData(data)
		forest.append(BuildTree(sample,entroFunc,splitCandFun))

	return forest

def ClassifyForest(data,trees):
	global resultMat 
	resultMat = [[] for i in range(len(data))]

	for i in range(len(data)):
		for node in trees:
		# fill the result into ith row in resultMat
			ClassifyTree(data[i],node,i)

	return resultMat

def ClassifyTree(data,node,i):
	# no more observations
	if len(data) == 0:
		return None

	# terminal node
	if node.label != None:
		resultMat[i].append(node.label.keys()[0])
		return None

	if data[node.attr] == node.cate:
		ClassifyTree(data,node.right,i)
	else:
		ClassifyTree(data,node.left,i)
	return None


def main():
	# train
	train_data = GetData(sys.argv[1])
	forest = BuildRandomForest(train_data,400,Gini,randomAttrCand)

	# get maxVote in random forest
	test_data = GetData(sys.argv[2])
	ClassifyForest(test_data,forest)
	result = []
	for row in resultMat:
		maxVote = max(set(row),key=row.count)
		result.append(maxVote)
	

	# fill out the confusion matrix
	num_labels = max(len(labelCount(train_data)),len(labelCount(test_data)))
	confusionMat = [[0]*num_labels for i in range(num_labels)]
	for i in range(len(test_data)):
		trueCate = int(test_data[i][0])
		predCate = int(result[i])
		confusionMat[trueCate-1][predCate-1] += 1

	# print confusion matrix
	for row in confusionMat:
		print(" ".join(map(str,row)))

if __name__ == '__main__':
	main()
