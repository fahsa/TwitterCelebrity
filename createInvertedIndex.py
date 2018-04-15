from pprint import pprint
import os
import preprocess as pro
import json


def indexDocument(tweet, celeb, invertedIndex, docLengths):
	tokens = pro.tokenizeText(tweet)
	noStops = pro.removeStopwords(tokens)
	# stems = pro.stemWords(noStops)

	if celeb not in docLengths:
		docLengths[celeb] = 0

	for term in noStops:
		docLengths[celeb] += 1
		if term not in invertedIndex:
			invertedIndex[term] = []
			invertedIndex[term].append(1)
			invertedIndex[term].append({})
			invertedIndex[term][1][celeb] = 1
		elif celeb not in invertedIndex[term][1]:
			invertedIndex[term][0] += 1
			invertedIndex[term][1][celeb] = 1
		elif celeb in invertedIndex[term][1]:
			invertedIndex[term][1][celeb] += 1

	return invertedIndex, docLengths


def main():
	path = os.getcwd() + '/celebrities/'
	invertedIndex = {}
	docLengths = {}

	for dir in os.listdir(path):
		if dir != '.DS_Store':
			directory = path + dir + '/'
			for file in os.listdir(directory):
				tweet = open(directory + file, 'r').read()
				invertedIndex, docLengths = indexDocument(tweet, dir, invertedIndex, docLengths)

	with open('invertedIndex.json', 'w') as fp:
		json.dump(invertedIndex, fp, indent=4)

	with open('docLengths.json', 'w') as out:
		json.dump(docLengths, out, indent=4)


if __name__ == '__main__':
	main()