
def mapTerm():
	dirs = ['pattern','max','closed','purity']
	files = [[open('{0}/{1}-{2}.txt'.format(dirs[i],dirs[i],j),'r') for j in range(5)] for i in range(4) ]
	output = [[open('{0}/{1}-{2}.txt.phrase'.format(dirs[i],dirs[i],j),'w') for j in range(5)] for i in range(4) ]
	
	# get the vocab list
	vocabFile = open('vocab.txt','r')
	vocab = vocabFile.readlines()
	vocab = [i.strip() for i in vocab]
	vocabFile.close()

	for i in range(4):
		for j in range(5):
			for line in files[i][j]:
				val = line.split()[0]
				idx = line.split()[1:]
				term = [vocab[int(num)] for num in idx]
				output[i][j].write(val+' '+' '.join(term)+'\n')
			files[i][j].close()
			output[i][j].close()


if __name__ == '__main__':
	mapTerm()