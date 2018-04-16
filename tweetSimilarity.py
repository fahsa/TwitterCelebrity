from __future__ import division
import os
import sys
import createInvertedIndex as cii
import preprocess as pro
import json
import math

celebs = ['Katy_Perry', 'Justin_Bieber', 'Barack_Obama', 'Rihanna', 'Kevin_Hart',
		  'Lady_Gaga', 'Ellen_DeGeneres', 'Justin_Timberlake', 'Kim_Kardashian',
		  'Britney_Spears', 'Ariana_Grande', 'Selena_Gomez', 'Demi_Lovato',
		  'Jimmy_Fallon', 'Donald_Trump', 'Bill_Gates', 'Oprah_Winfrey', 'Bruno_Mars',
		  'LeBron_James', 'Miley_Cyrus']


def preprocessTweet(tweet):
	tokens = pro.tokenizeText(tweet)
	noStops = pro.removeStopwords(tokens)

	return noStops


def weighting(tweets, celebIndex, celeb):
    user_tf = {}
    dot_product = 0

    for word in tweets:
        if word in celebIndex:
            if word not in user_tf:
                user_tf[word] = 0
            user_tf[word] += 1

    for word, freq in user_tf.items():
        user_tfidf = 0
        celeb_tfidf = 0

        idf = math.log(20/(celebIndex[word][0]))

        user_tfidf = freq * idf

        if celeb in celebIndex[word][1]:
            celeb_tfidf = celebIndex[word][1][celeb] * idf

        dot_product += user_tfidf * celeb_tfidf

    return dot_product


def run_rocchio_method(folder):
	tweetDirectory = folder
	path = os.getcwd() + '/' + tweetDirectory + '/'

	output = open('rocchio.out', 'w+')
	
	with open('invertedIndex.json', 'r') as handle:
		celebIndex = json.load(handle)

	with open('docLengths.json', 'r') as lengths:
		docLengths = json.load(lengths)


	tweet = ''
	numCorrect = 0
	total = 0
	for file in os.listdir(path):
		addition = ' ' + open(path + file, 'r').read()
		tweet += addition
		#tweet = open(path + file, 'r').read()

	tokens = preprocessTweet(tweet)

	if len(tokens) == 0:
		return

	similarities = {}
	for celeb in celebs:
		inner_product = weighting(tokens, celebIndex, celeb)
		similarities[celeb] = float(inner_product/(len(tokens) * docLengths[celeb]) * 10000)

	num = 0
	#total += 1
	sortedVal = [(k, similarities[k]) for k in sorted(similarities, key=similarities.get, reverse=True)]
	for key, val in sortedVal:
		if num < 3:
			name = str(key).replace('_', ' ')
			output.write(name + '\n' + str(val) + '\n')
			#output.write(str(key) + '\n')
			# if file.startswith(key):
			# 	numCorrect += 1
			num += 1

	#output.write("Accuracy = " + str(numCorrect/total))








if __name__ == '__main__':
	run_rocchio_method(sys.argv[1])