# Nick Shahin
# shahinna
# Code modified from Project 1 Part 2: Language Identification

import re
import sys
import os
import math

def run_bigram_word_method():
    celeb_pos = []
    word_frequencies = []
    word_bigrams = []
    lengths = []
    train_dir = "celebrities/"
    test_celebs = os.listdir(train_dir)
    for celeb in test_celebs:
        count = 0
        if celeb == ".DS_Store":
            continue
        cur_dir = train_dir+celeb+"/"
        temp = trainBigramModel(cur_dir)
        word_frequencies.append(temp[0])
        word_bigrams.append(temp[1])
        lengths.append(temp[2])
        celeb_pos.append(celeb)

    test_dir = "testUser/"
    test_text = ""
    for tweet in os.listdir(test_dir):
        test_file = open(test_dir+tweet, 'r')
        tweet_text = test_file.read()
        test_file.close()
        test_text = test_text + " " + tweet_text
    celebs = identifyCelebrity(test_text, celeb_pos, word_frequencies, word_bigrams, lengths)
    #print(celeb)

def trainBigramModel(tweet_directory):
    word_frequencies = {}
    word_bigram = {}
    total_chars = 0
    length = 0

    for tweet in os.listdir(tweet_directory):
        input_file = open(tweet_directory+tweet, 'r')
        input_string = input_file.read()
        input_file.close()
        length = length + len(input_string)
        input_string = input_string.replace("\n", " ")
        input_string = input_string.split(" ")

        # Character frequencies
        for c in input_string:
            if c not in word_frequencies:
                word_frequencies[c] = 1
            else:
                word_frequencies[c] = word_frequencies[c] + 1
            total_chars+=1

        # Character-bigram frequencies
        idx = 1
        while idx < len(input_string):
            bigram = input_string[idx-1] + input_string[idx]
            if bigram not in word_bigram:
                word_bigram[bigram] = 1
            else:
                word_bigram[bigram] = word_bigram[bigram] + 1
            idx+=1

    return(word_frequencies, word_bigram, length)

def identifyCelebrity(test_text, celeb_list, word_frequencies, word_bigrams, lengths):
    pos = 0
    test_text = test_text.replace("\n", " ")
    test_text = test_text.split(" ")
    probabilities = []

    while pos < len(celeb_list):
        probabilities.append(0.0)
        idx = 0
        while idx < len(test_text)-1:
            bigram_count = 1
            char_count =  int(len(word_frequencies[pos]))

            bigram = test_text[idx] + test_text[idx+1]
            if bigram in word_bigrams[pos]:
                bigram_count = word_bigrams[pos][bigram] + 1

            if test_text[idx] in word_frequencies[pos]:
                char_count = word_frequencies[pos][test_text[idx]] + char_count

            fraction = float(bigram_count) / float(char_count)
            logged_fraction = math.log10(fraction)
            if probabilities[pos] == 0:
                probabilities[pos] = logged_fraction
            else:
                probabilities[pos] = probabilities[pos] + logged_fraction

            idx+=1
        pos+=1
    
    idx = 0
    output_file = open("word_output", "w")

    while idx < 3:
        name = celeb_list[probabilities.index(max(probabilities))].replace("_", " ")
        output_file.write(name+"\n1\n")
        del celeb_list[probabilities.index(max(probabilities))]
        del probabilities[probabilities.index(max(probabilities))]
        idx+=1
    output_file.close()
    return celeb_list[probabilities.index(max(probabilities))]

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run_bigram_word_method()
