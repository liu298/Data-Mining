## step 2.2 2 Tokenize Plain Text by Dictionary (10pts)
# In this step, we represent each title as a sparse vector of word counts. 
# We ask you to transform each title (i.e., each line in paper.txt) into 
# the following format ([M] (space) [t1]:[c1] (space) [t2]:[c2] (space) ...):
# [M] [term_1]:[count] [term_2]:[count] ...  [term_N]:[count]

# where [M] is the number of unique terms in the title, 
# and the [count] associated with each term is how many times 
# that term appeared in the title. For example, in paper.txt, 
# suppose we have a title "automatic acquisition proof method". 
# The corresponding line in the output file should be "4 0:1 1:1 2:1 3:1". 
# Note that [term_i] is an integer which indexed a term in vocab.txt; 
# it starts from 0. Please name the output file as title.txt.


def main():
	title = []
	output = open('title.txt','w')
	vocabFile = open('vocab.txt','r')
	vocab = vocabFile.readlines()
	vocab = [i.strip() for i in vocab]
	vocabFile.close()
	with open('paper.txt','r') as file:
		text = file.readlines()
		for line in text:
			words = line.split("\t")[1].split()
			titleLine = str(len(set(words))) + " "
			for i in set(words):
				titleLine += str(vocab.index(i)) +":"+str(words.count(i))+" "
			title.append(titleLine)
	output.write("\n".join(title))
	output.close()


if __name__ == '__main__':
	main()


# LDA command 
#lda-c-dist/lda est 0.001 5 lda-c-dist/settings.txt title.txt  random  result