import os

if __name__ == '__main__':
	with open('topic-0.txt','r') as input:
		with open('patterns/test.txt','w') as output:
			for line in input:
				output.write(line)
	os.makedirs('test_dir')