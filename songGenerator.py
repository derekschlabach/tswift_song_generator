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

#rhyme scheme and line count need to match up
#song_structure = [lineCount, syllX, syllY, rhymeScheme, unique] 
part_structure = {}
part_structure['v'] = [4, 12, 16, [0,1,0,1], 1]
part_structure['c'] = [6, 12, 16, [1,0,0,1,1,0], 0]
part_structure['pc'] = [2, 8, 12, [0,1], 0]
part_structure['b'] = [3, 16, 20, [1,0,1], 0]

song_structure = ['v', 'v', 'pc', 'c', 'v', 'c', 'b', 'c']

stored_part = {}

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
        


 
def get_word_for_pos(select_vocab, hist):
    word_probs = {}
    sumProbs = 0.0
    
    for word in select_vocab :
        prob = langmod.p(word, hist)
        word_probs[word] = prob
        sumProbs += word_probs[word]
    
    if sumProbs == 0.0:
        for word in select_vocab :
            prob = langmod.p(word, hist[-1])
            word_probs[word] = prob
            sumProbs += word_probs[word]
    
    if sumProbs == 0.0:
        for word in select_vocab:
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
    
song = ""
    
rhymeLevel = 2
for ind in song_structure:
    part = part_structure[ind]
    currLineCount = part[0]
    currSyllX = part[1]
    currSyllY = part[2]
    currRhymeScheme = part[3] 
    currUnique = part[4]

    part_to_build = ""

    if not currUnique and ind in stored_part :
        print stored_part[ind]
        continue
        
    rhymeSchemeIndex = 0
    #first is the 0 rhyming word, second is the 1 rhyme, third is last part of speech line ending
    previous = ['0', '1', '0']
    #for however many lines this part of the song should be
    line = 0
    while line < currLineCount :
        #if this isn't the first line
        line_passes = True
        if previous[2] != '0':
            #loop until we find a valid sentence ending that also rhymes
            while True:
                struct = line_structures[int(random.random() * len(line_structures))]
                if struct[-1] in valid_line_transitions[previous[2]]:
                    break
        #if this is the first, then save the last part of speech to check against next iteration
        else:
            struct = line_structures[int(random.random() * len(line_structures))]
            previous[2] = struct[-1]

                
        line_to_build = []
            
        for i in xrange(len(struct)) :
            pos = struct[i]

            #if we are at the last pos in the struct 
            if i == len(struct)-1:
                #if previous at the current rhyme scheme's value is not initialized
                currPrevious = previous[currRhymeScheme[line]]
                if currPrevious == '0' or currPrevious == '1':

                    line_to_build.append(get_word_for_pos(words_in_pos[pos], line_to_build))
                    #record the last word so we can rhyme with it
                    previous[currRhymeScheme[line]] = line_to_build[-1]
                    rhymeSchemeIndex += 1
                #if the value for the one we are on has been initialized 
                else:

                    word_to_rhyme = currPrevious
                    #pass this set to get_word_for_pos maybe but for now just iterate until good
                    rhyming_words = rhyme(word_to_rhyme, words_in_pos[pos], rhymeLevel)
                    #print rhyming_words

                    if len(rhyming_words) > 0 :
                        line_to_build.append(get_word_for_pos(rhyming_words, line_to_build))
                        #rhymeSchemeIndex += 1
                    else :
                        line_passes = False
            else:
                line_to_build.append(get_word_for_pos(words_in_pos[pos], line_to_build))


        num_syll = syllables(" ".join(line_to_build))
        if num_syll < currSyllX or num_syll > currSyllY  :
            line_passes = False
    
            
                    
        if line_passes :
            line += 1 
            line_str = re.sub(r' i\b', ' I', " ".join(line_to_build).capitalize())
            part_to_build += line_str + '\n'

    if not currUnique :
        stored_part[ind] = part_to_build 

    print part_to_build + "\n"
