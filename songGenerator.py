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

#make map of pos to sets of words of that pos from nltk's tags
words_in_pos = {}
for tag in reduced_tagset :
   words_in_pos[tag] = []

line_structures = []   

for line in raw_lines:
    tagged_line = nltk.pos_tag(nltk.Text(re.findall(r'[a-z\'0-9]+', line)))
    currentStruct = [ reduced_tgs[tag] for (word, tag) in tagged_line ]
    
    for (word, tag) in tagged_line :
        tag = reduced_tgs[tag]
        if word not in words_in_pos[tag] :
            words_in_pos[tag].append(word)      

    if line_structures is None or currentStruct not in line_structures:
        line_structures.append(currentStruct)
        

#print "line_structures:" + str(line_structures[:10]) + '\n'
#print "Number of line_structures:" + str(len(line_structures))


#print words_in_pos
 
def get_word_for_pos(pos, hist):
    word_probs = {}
    sumProbs = 0.0
    
    #print words_in_pos[pos]
    for word in words_in_pos[pos]:
        prob = langmod.p(word, hist)
        word_probs[word] = prob
        sumProbs += word_probs[word]
    
    if sumProbs == 0.0:
        for word in words_in_pos[pos]:
            prob = langmod.p(word, hist[-1])
            word_probs[word] = prob
            sumProbs += word_probs[word]
    
    if sumProbs == 0.0:
        for word in words_in_pos[pos]:
            prob = langmod.p(word, [''])
            word_probs[word] = prob
            sumProbs += word_probs[word]
    
    #choose random number from 0.00000001 to sumProbs (inclusive)
    rand = random.random() * sumProbs
    print str(sumProbs) + ": " + str(rand)
    counter = 0.0
    for word in word_probs:
        counter += word_probs[word]
        if counter >= rand:
            #this is the word that we have chosen based on the weighted probabilities
            return word
        
    #if we do not return anything we should throw an exception
    
struct = line_structures[int(random.random() * len(line_structures))]
line_to_build = []

for pos in struct:
    line_to_build.append(get_word_for_pos(pos, line_to_build))
for i in range(10) :
    print get_word_for_pos('NS', [])

print "Length of line_to_build:" + str(len(line_to_build))
print struct
print line_to_build



'''
for pos in words_in_pos :
    print str(len(words_in_pos[pos])) + ": " +  pos
    print words_in_pos[pos]

    print
    print
'''



#print nltk_text
