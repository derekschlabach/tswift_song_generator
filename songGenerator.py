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
reduced_tgs = {}

#Singular Nouns
for x in ['NN', 'NNP']: reduced_tgs[x] = 'NS'

#Plural Nouns
for x in ['NNS', 'NNPS']: reduced_tgs[x] = 'NP'
    
#There
reduced_tgs['EX'] = 'EX'

#Personal Pronouns
reduced_tgs['PRP'] = 'PRP'

#Wh-Pronouns
reduced_tgs['WP'] = 'WP'

#Verbs should stay the same to preserve tense and tone
reduced_tgs['VB']  = 'VB'
reduced_tgs['VBD'] = 'VBD'
reduced_tgs['VBG'] = 'VBG'
reduced_tgs['VBN'] = 'VBN'
reduced_tgs['VBP'] = 'VBP'
reduced_tgs['VBZ'] = 'VBZ'
reduced_tgs['MD']  = 'MD'
reduced_tgs['TO']  = 'TO'

#Possesive Pronoun
reduced_tgs['PRP$']  = 'PRP$'

#Determiner
reduced_tgs['DT'] = 'DT'

#Cardinal Numbers
reduced_tgs['CD'] = 'CD'

#Which
reduced_tgs['WDT'] = 'WDT'

#Adjective-Like
for x in ['JJ', 'JJR', 'JJS']: reduced_tgs[x] = 'AJ'

#Wh-adverbs
reduced_tgs['WRB'] = 'WRB'

#Prepositions
for x in ['RP', 'IN']: reduced_tgs[x] = 'IN'

#Coordinating Conjunctions
reduced_tgs['CC'] = 'CC'

#Adverb-Like
for x in ['RB', 'RBR', 'RBS']: reduced_tgs[x] = 'AV'

# end-of-sentence symbols
reduced_tgs['-NONE-'] = '-NONE-'

print len(set(reduced_tgs.values()))

#reduced_tags = ['N', 'V', 'AJ', 'AV', 'I', 'S', 'G', 'E']


#use nltk tags not reduced
#make map of pos to sets of words of that pos from nltk's tags
words_in_pos = {}
all_tagged_vocab = nltk.pos_tag(nltk.Text(vocab))
#all_tagged_vocab = [ (word, reduced_tgs[tag]) for (word, tag) in all_tagged_vocab ]
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
        #swap these with the reduced tagset here and only keep those structures
        currentStruct.append(reduced_tgs[tag])
    #print currentStruct
    if line_structures is None or currentStruct not in line_structures:
        line_structures.append(currentStruct)
        
    counter += 1
print "line_structures:" + str(line_structures[:10]) + '\n'
print "Number of line_structures:" + str(len(line_structures))

#Function to return a random word from a pos based on weighted probability 
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
    
struct = line_structures[(random.random() * len(line_structures))]
line_to_build = ['']
print "Length of line_to_build:" + str(len(line_to_build))
for pos in struct:
    get_word_for_pos(words_in_pos[pos], line_to_build, langmod)



'''
for pos in words_in_pos :
    print str(len(words_in_pos[pos])) + ": " +  pos
    print words_in_pos[pos]

    print
    print
'''



#print nltk_text
