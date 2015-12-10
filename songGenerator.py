#@author Kyle Kent Derek Schlabach
import nltk
from nltk.corpus import PlaintextCorpusReader
from custom.langmod import *

import re
import random

file_name = "corpus/tswift-full.txt"
raw_words = re.findall(r'[a-z\'0-9]+', file(file_name).read().lower())
nltk_text = nltk.Text(raw_words)
vocab = set(raw_words)

lm_data = LanguageModelData(raw_words)
langmod = TrigramLanguageModel(lm_data)

#use nltk tags not reduced
#make map of pos to sets of words of that pos from nltk's tags
words_in_pos = {}
#all_tagged = nltk.pos_tag(nltk_text)
all_tagged_vocab = nltk.pos_tag(nltk.Text(vocab))
for (word, tag) in all_tagged_vocab :
    if tag in words_in_pos :
        words_in_pos[tag].append(word)
    else :
        words_in_pos[tag] = [word]

#print words_in_pos
for pos in words_in_pos :
    print pos
    print words_in_pos[pos]

    print
    print

 
def get_word_for_pos(pos, hist):
    word_probs = {}
    sumProbs = 0.0
    for word in words_in_pos[pos]:
        word_probs[word] = langmod.p(word, hist)
        sumProbs += word_probs[word]
    
    #choose random number from 0.00000001 to sumProbs (inclusive)
    rand = random.random() * sumProbs
    counter = 0.0
    for word in word_probs:
        counter += word_probs[word]
        if counter >= rand:
            #this is the word that we have chosen based on the weighted probabilities
            return word
        
    #if we do not return anything we should throw an exception
        
#print nltk_text
