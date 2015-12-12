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

lineCount = 4
syllX = 12
syllY = 16
rhymeScheme = 0101
#rhyme scheme and line count need to match up
song_structure = {'Verse':[lineCount, syllX, syllY, rhymeScheme], 
                  'Chorus':[6, 12, 16, 100110]}

line_structures = []
#this should be a map of every possible line ending to every possible line beginning that can follow
valid_line_transitions = {}   
previous = '0'
for line in raw_lines:
    tagged_line = nltk.pos_tag(nltk.Text(re.findall(r'[a-z\'0-9]+', line)))
    currentStruct = [ reduced_tgs[tag] for (word, tag) in tagged_line ]
    
    for (word, tag) in tagged_line :
        #print word, tag
        indexTag = tag #need this because reduced tags are not in tagged line
        tag = reduced_tgs[tag]
        if word not in words_in_pos[tag] :
            words_in_pos[tag].append(word)
    
        if tagged_line.index((word, indexTag)) == len(tagged_line)-1:
            if previous == 0 or previous not in valid_line_transitions:
                valid_line_transitions[previous] = set()
            
            else:
                valid_line_transitions[previous].add(tag)
            previous = tag

    if line_structures is None or currentStruct not in line_structures:
        line_structures.append(currentStruct)
        
#print "valid transitions:" + str(valid_line_transitions) + '\n'
        
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
            prob = langmod.p(word, [])
            word_probs[word] = prob
            sumProbs += word_probs[word]
    
    #choose random number from 0.00000001 to sumProbs (inclusive)
    rand = random.random() * sumProbs
    #print str(sumProbs) + ": " + str(rand)
    counter = 0.0
    for word in word_probs:
        counter += word_probs[word]
        if counter >= rand:
            #this is the word that we have chosen based on the weighted probabilities
            return word
        
    #if we do not return anything we should throw an exception
    
    
for part in song_structure:
    currLineCount = part[0]
    currSyllX = part[1]
    currSyllY = part[2]
    #1s and 0s need to rhyme with each other
    currRhymeScheme = part[3] #0101
    rhymeSchemeIndex = 0
    #first is the 0 rhyming word, second is the 0 rhyme, third is last part of speech 
    previous = ('0', '1', '0')
    #for however many lines this part of the song should be
    for line in range(currLineCount):
        #if this isn't the first line
        if previous[2] != '0':
            #loop until we find a valid sentence ending that also rhymes
            while True:
                struct = line_structures[int(random.random() * len(line_structures))]
                #print struct[-1]
                if struct[-1] in valid_line_transitions[previous[2]]:
                    break
        #if this is the first, then save the last part of speech to check against next iteration
        else:
            struct = line_structures[int(random.random() * len(line_structures))]
            previous[2] = struct[-1]

                
        line_to_build = []
            
        for pos in struct:
            #if we are at the last pos in the struct 
            if struct.index(pos) == len(struct)-1:
                #if previous at the current rhyme scheme's value is not initialized
                if previous[currRhymeScheme[rhymeSchemeIndex]] == '0' or '1':
                    line_to_build.append(get_word_for_pos(pos, line_to_build))
                    #record the last word so we can rhyme with it
                    previous[currRhymeScheme[rhymeSchemeIndex]] = line_to_build[-1]
                    rhymeSchemeIndex += 1
                #if the value for the one we are on has been initialized 
                else:
                    word_to_rhyme = previous[currRhymeScheme[rhymeSchemeIndex]]
                    #pass this set to get_word_for_pos maybe but for now just iterate until good
                    rhyming_words = rhyme(word_to_rhyme, words_in_pos[pos])
                    candidate_word = ''
                    while True:
                        candidate_word = get_word_for_pos(pos, line_to_build)
                        if candidate_word in rhyming_words:
                            line_to_build.append(candidate_word)
                            break
                    
                    
            

        
        
    
        print "Length of line_to_build:" + str(len(line_to_build))
        print struct
        print line_to_build
    
prev_ending = '0'
for x in range(0, 10):
    #if this isn't the first line
    if prev_ending != '0':
        
        while True:
            struct = line_structures[int(random.random() * len(line_structures))]
            #print struct[-1]
            if struct[-1] in valid_line_transitions[prev_ending]:
                break
    
    else:
        struct = line_structures[int(random.random() * len(line_structures))]
        prev_ending = struct[-1]
        
    line_to_build = []
    
    for pos in struct:
        line_to_build.append(get_word_for_pos(pos, line_to_build))
    

    #for i in range(10) :
    #   print get_word_for_pos('NS', [])
    
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
