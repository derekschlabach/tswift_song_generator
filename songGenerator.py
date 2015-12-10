@author Kyle Kent Derek Schlabach
import nltk
from nltk.corpus import PlaintextCorpusReader
import sys
import re
from nltk import FreqDist

#Taken from project 3
file_name = "corpus/tswift-full.txt"
raw_words = re.findall(r'[a-z][a-z\']*|\d+|[!$%*()\-:;\"\',.?]', file(file_name).read().lower())
vocab = set(raw_words)

class LanguageModelData:    
    def __init__(self, text):
        self.fd_unigrams = FreqDist(text)
        self.fd_bigrams = FreqDist([tuple(text[i:i+2]) for i in range(len(text) - 1)])
        self.fd_trigrams = FreqDist([tuple(text[i:i+3]) for i in range(len(text) - 2)])
        self.N = len(text)
        #self.count_of_counts = FreqDist([self.fd_unigrams[w] for w in vocab])

    def unigram_count(self, w):
        return float(self.fd_unigrams[w])
    
    def bigram_count(self, w1, w2):
        return float(self.fd_bigrams[(w1, w2)])
        
    def trigram_count(self, w1, w2, w3):
        return float(self.fd_trigrams[(w1, w2, w3)])

#Taken from project 3
class TrigramLanguageModel :
    def __init__(self, lm_data):
        self.lm_data = lm_data
        
    def p(self, w, h):
        try :
            if len(h) == 0 :
                return float(self.lm_data.fd_unigrams[w]) / self.lm_data.N
            elif len(h) == 1 :
                return float(self.lm_data.fd_bigrams[(h[0], w)]) / self.lm_data.fd_unigrams[h[-1]]
            else :
                return float(self.lm_data.fd_trigrams[(h[-2], h[-1], w)]) / self.lm_data.fd_bigrams[(h[-2], h[-1])]
        except ZeroDivisionError :
            return 0.0

    def kind_of_model(self):
        return "trigram"

alphabet = "abcdefghijklmnopqrstuvwxyz'"

def transform(w):
    if w.isdigit():
        return "NUM"    
    elif all(c in alphabet for c in w) :
        if w in vocab :
            return w
        else :
            return "OOV"
    else :
        return  "PNCT"

lm_data = LanguageModelData([transform(w) for w in raw_words])


#use nltk tags not reduced
#make map of pos to sets of words of that pos from nltk's tags
words_in_pos = {}
langmod = TrigramLanguageModel(lm_data)


    
def get_word_for_pos(pos, hist):
    word_probs = {}
    sumProbs = 0.0
    for word in words_in_pos[pos]:
        word_probs[word] = langmod.p(word, hist)
        sumProbs += word_probs[word]
    
    #choose random number from 0.00000001 to sumProbs (inclusive)
    rand = 0.0
    counter = 0.0
    for word in word_probs:
        counter += word_probs[word]
        if counter >= rand:
            #this is the word that we have chosen based on the weighted probabilities
            return word
        
    #if we do not return anything we should throw an exception
        
    
    
    