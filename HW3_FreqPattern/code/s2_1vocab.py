## step 2.1 create vocab.txt


def main():
	vocab = []
	output = open('vocab.txt','w')
	with open('paper.txt','r') as file:
		text = file.readlines()
		for line in text:
			words = line.split("\t")[1]
			for word in words.split():
				if word not in vocab:
					vocab.append(word)
	output.write("\n".join(vocab))
	output.close()


if __name__ == '__main__':
	main()
	
			