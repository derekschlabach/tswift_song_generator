#@author Kyle Kent Derek Schlabach
import nltk
from nltk.corpus import PlaintextCorpusReader
from custom.langmod import *
from custom.functions import *

import re
import random

file_name = "corpus/tswift-full.txt"

raw_lines = filter(None, [ re.sub(r'\([^)]*\)|^[a-z\'0-9]', '', line).strip().lower() for line in open(file_name).readlines()])

raw_words = re.findall(r'[a-z\'0-9]+', ' '.join(raw_lines))
vocab = set(raw_words)

#in custom.langmod
lm_data = LanguageModelData(raw_words)
langmod = TrigramLanguageModel(lm_data)

#Taken from Proj 4
penntb_to_reduced = {}
# noun-like
for x in ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'EX', 'WP'] :
    penntb_to_reduced[x] = 'N'
# verb-like
for x in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD', 'TO'] :
    penntb_to_reduced[x] = 'V'
# adjective-like
for x in ['POS', 'PRP$', 'WP$', 'JJ', 'JJR', 'JJS', 'DT', 'CD', 'PDT', 'WDT', 'LS']:
    penntb_to_reduced[x] = 'AJ'
# adverb-like
for x in ['RB', 'RBR', 'RBS', 'WRB', 'RP', 'IN', 'CC']:
    penntb_to_reduced[x] = 'AV'
# interjections
for x in ['FW', 'UH'] :
    penntb_to_reduced[x] = 'I'
# symbols
for x in ['SYM', '$', '#'] :
    penntb_to_reduced[x] = 'S'
# groupings
for x in ['\'\'', '(', ')', ',', ':', '``'] :
    penntb_to_reduced[x] = 'G'
# end-of-sentence symbols
penntb_to_reduced['.'] = 'E'
penntb_to_reduced['-NONE-'] = '-NONE-'

reduced_tags = ['N', 'V', 'AJ', 'AV', 'I', 'S', 'G', 'E']


#use nltk tags not reduced
#make map of pos to sets of words of that pos from nltk's tags
words_in_pos = {}
all_tagged_vocab = nltk.pos_tag(nltk.Text(vocab))
#all_tagged_vocab = [ (word, penntb_to_reduced[tag]) for (word, tag) in all_tagged_vocab ]
for (word, tag) in all_tagged_vocab :
    if tag in words_in_pos :
        words_in_pos[tag].append(word)
    else :
        words_in_pos[tag] = [word]

line_structures = []   
counter = 0 
for line in raw_lines:
    #if counter is 10:
     #   break
    currentStruct = []
    tagged_line = nltk.pos_tag(nltk.Text(line.split(' ')))
    for (word, tag) in tagged_line:
        #print word, tag
        currentStruct.append(tag)
    #print currentStruct
    if line_structures is None or currentStruct not in line_structures:
        line_structures.append(currentStruct)
        
    counter += 1
print "line_structures:" + str(line_structures[:10]) + '\n'
print "Number of line_structures:" + str(len(line_structures))


'''
for pos in words_in_pos :
    print str(len(words_in_pos[pos])) + ": " +  pos
    print words_in_pos[pos]

    print
    print
'''


 
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
