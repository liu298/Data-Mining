## step 3.2 Re-organize the Terms by Topic (5pts)
# You are asked to re-organize the terms by 5 topics. 
# For the i-th topic, you should create a file named topic-i.txt. 
# Separate each line in word-assignment.dat by topics assigned to them. 
# For example, the lines in word-assignment.dat can be considered as the following form 
# ( Note that here we replace the integers with the real terms for better illustration):

# 004 automatic:02 acquisition:02 proof:02 method:02 
# 005 classification:03 noun:02 phrase:03 concept:01 individual:03

### argv: result/word-assignments.dat
### create topic files


import sys

def main():
	count = 0
	output = [open('topic-{}.txt'.format(i),'w') for i in range(5)]
	with open(sys.argv[1], 'r') as input:
	  for line in input:
	  	words = line.split()[1:]
	  	# write words in this line into certain file
	  	tpAdd = []
	  	for item in words:
	  		(word,ti) = item.split(':')
	  		tpAdd += [int(ti)] 
	  		output[int(ti)].write(word+" ")
	  	# write a newline in last changed output files
	  	for i in set(tpAdd):
	  		output[i].write('\n')	  	

	for fin in output:
		fin.close()
	      
if __name__ == '__main__':
	main()

