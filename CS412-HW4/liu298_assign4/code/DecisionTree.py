# Step 2: Implement Basic Classification Method

import sys

class Node:
	def __init__(self,attr=-1,cate=-1,left=None,right=None,label=None):
		"""
		:type attr: int
		:type value: int
		"""
		self.attr = attr
		self.cate = cate
		self.left = left
		self.right = right
		self.label = label

	# def __str__(self):
	# 	if label != None:
	# 		return str(label)
	# 	return (str(self.attr)+" "+str(self.value))

def GetData(file):
	attrs = []
	with open(file) as fin:
		for line in fin:
			if line.strip() != "":
				label = line.strip().split()[0]
				vals = line.strip().split()[1:]
				row = [label]
				for i in vals:
					key,val = map(int,i.split(':'))
					row.append(val)
				attrs.append(row)
			
	return attrs


def Gini(data):
	labels = labelCount(data)
	count = sum(labels.values())
	return 1-sum(map(lambda x:pow(x/float(count),2),labels.values()))

def labelCount(data):
	label = {}
	for i in data:
		if i[0] not in label: label[i[0]] = 0
		label[i[0]] += 1
	return label

# devide the set into 2 parts according to certain attr and cate
# return data of 2 parts
def split(data,attr,cate):
	true = list(filter(lambda x: x[attr] == cate, data))
	false = list(filter(lambda x: x[attr] != cate, data))
	return (false,true)

def BuildTree(data,entroFunc,splitCandFun):
	# no observations
	if len(data) == 0:
		return None

	labels = labelCount(data)
	# only one label
	if len(labels) == 1:
		return Node(label=labels)

	leastGini = entroFunc(data)
	splitAttr = None
	splitCate = None
	splitSet = None

	splitCate = splitCandFun(data)
	# print("splitCate",splitCate)
	for attr, cate in splitCate:
		(false,true) = split(data,attr,cate)

		newGini = sum(map(lambda x: len(x)/float(len(data))*entroFunc(x),(false,true)))
		if newGini < leastGini:
			leastGini = newGini
			splitAttr = attr
			splitCate = cate
			splitSet = (false,true)

	# print("new Gini", leastGini)
	# print("attr, cate ",splitAttr, splitCate)
	# print("false",splitSet[0])
	# print("true",splitSet[1])

	# no remaining attr makes information gain
	# make the terminal node the maximum vote label
	if leastGini == entroFunc(data):
		maxVote = max(labels,key=lambda x:labels[x])
		retDict = {maxVote:labels[maxVote]}
		return Node(label=retDict)

	left = BuildTree(splitSet[0],entroFunc,splitCandFun)
	right = BuildTree(splitSet[1],entroFunc,splitCandFun)
	return Node(splitAttr,splitCate,left,right)


def splitCand(data):
	candidates = []
	for row in data:
		for i in range(1,len(row)):
			if (i,row[i]) not in candidates:
				candidates.append((i,row[i]))
	return candidates

def ClassificationTree(data,tree):
	# terminal node
	if tree.label != None:
		labels = labelCount(data)
		for i in map(int,labels.keys()):
			for j in map(int,tree.label.keys()):
				confusionMat[i-1][j-1] += labels[str(i)]

		return Node(label=labels)

	# no more observations
	if len(data) == 0:
		return None

	(false,true) = split(data,tree.attr,tree.cate)
	left = ClassificationTree(false,tree.left)
	right = ClassificationTree(true,tree.right)
	return Node(tree.attr,tree.cate,left,right)

def main():
	# train
	train_data=GetData(sys.argv[1])
	tree = BuildTree(train_data,Gini,splitCand)

	# test
	test_data = GetData(sys.argv[2])
	num_labels = max(len(labelCount(train_data)),len(labelCount(test_data)))
	global confusionMat
	confusionMat = [[0]*num_labels for i in range(num_labels)]

	newTree = ClassificationTree(test_data,tree)

	# print confusion matrix
	for row in confusionMat:
		print(" ".join(map(str,row)))


if __name__ == '__main__':
	main()