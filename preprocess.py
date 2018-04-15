#Name: Amy Rechkemmer
#Uniqname: rechkamy

import sys
import os
import re
import operator
import Porter_stemmer_code

stopwords = open('stopwords', 'r').read().split('\n')

contractions = {
	"aren't": "are not",
	"can't": "cannot",
	"could've": "could have",
	"couldn't": "could not",
	"didn't": "did not",
	"doesn't": "does not",
	"don't": "do not",
	"gonna": "going to",
	"gotta": "got to",
	"hadn't": "had not",
	"hasn't": "has not",
	"haven't": "have not",
	"he'd": "he would",
	"he'll": "he will",
	"he's": "he is",
	"how'd": "how did",
	"how'll": "how will",
	"how's": "how is",
	"i'd": "i would",
	"i'll": "i will",
	"i'm": "i am",
	"i've": "i have",
	"isn't": "is not",
	"it'd": "it would",
	"it'll": "it will",
	"it's": "it is",
	"let's": "let us",
	"ma'am": "madam",
	"mayn't": "may not",
	"may've": "may have",
	"mightn't": "might not",
	"might've": "might have",
	"mustn't": "must not",
	"must've": "must have",
	"needn't": "need not",
	"o'clock": "of the clock",
	"oughtn't": "ought not",
	"shan't": "shall not",
	"she'd": "she would",
	"she'll": "she will",
	"she's": "she is",
	"should've": "should have",
	"shouldn't": "should not",
	"that'll": "that will",
	"that's": "that is",
	"that'd": "that would",
	"there'd": "there would",
	"there's": "there is",
	"they'd": "they would",
	"they'll": "they will",
	"they're": "they are",
	"they've": "they have",
	"wasn't": "was not",
	"we'd": "we would",
	"we'll": "we will",
	"we're": "we are",
	"we've": "we have",
	"weren't": "were not",
	"what'd": "what did",
	"what'll": "what will",
	"what're": "what are",
	"where's": "where is",
	"who'll": "who will",
	"who're": "who are",
	"who's": "who is",
	"why'd": "why did",
	"won't": "will not",
	"would've": "would have",
	"wouldn't": "would not",
	"you'll": "you will",
	"you're": "you are",
	"you've": "you have"
}

punctuation = ['.', ',', ';', ':', '?', '!', '"', '(', ')', '<', '>', '[', ']',
			   '*', '#', '@', '%', '^', '&']

def removeSGML(inputString):
	outputString = re.sub(r'\<.+\>','',inputString)
	return outputString


def tokenizeText(inputString):
	outputString = inputString.lower()
	for punc in punctuation:
		outputString = outputString.replace(punc, "")
	wordList = outputString.split()
	outputList = []
	for word in wordList:
		if not word.isdigit():
			if word in contractions:
				newWords = contractions[word].split()
				for newWord in newWords:
					outputList.append(newWord)
			elif word.endswith("'s"):
				outputList.append(word[:-2])
				outputList.append("'s")
			else:
				outputList.append(word)

	return outputList


def removeStopwords(inputList):
	outputList = []
	for value in inputList:
		if value not in stopwords:
			outputList.append(value)

	return outputList

def stemWords(inputList):
	stemmedOutput = []
	p = Porter_stemmer_code.PorterStemmer()
	for token in inputList:
		stemmedOutput.append(p.stem(token, 0, len(token) - 1))

	return stemmedOutput

def main():
	wordCount = open('preprocess.output', 'w+')
	answersFiles = ["cranfield0001", "cranfield0002"]
	path = os.getcwd() + "/" + sys.argv[1]
	dictionary = {}
	totWords = 0
	for file in os.listdir(path):
	#for file in answersFiles:
		doc_words = open(path + file, 'r').read()
		noSGML = removeSGML(doc_words)
		tokens = tokenizeText(noSGML)
		noStops = removeStopwords(tokens)
		stems = stemWords(noStops)

		for stem in stems:
			if stem not in dictionary:
			  dictionary[stem] = 0
			dictionary[stem] += 1
			totWords += 1

	wordCount.write("Words " + str(totWords) + '\n')
	wordCount.write("Vocabulary " + str(len(dictionary)) + '\n')
	wordCount.write("Top 50 words" + '\n')

	for i in range(50):
		top = max(dictionary.iteritems(), key=operator.itemgetter(1))
		wordCount.write("Word" + str(i + 1) + " " + str(top[1]) + '\n')
		del dictionary[top[0]]

if __name__ == '__main__':
	main()
	