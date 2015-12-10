#author Kyle Kent
from custom.functions import *
import nltk 

while True :
    vars = raw_input("Enter the target word and level(int) followed by candidates ").split(' ')
    #print "Inputs:" + str(vars) +"\n"
    target = vars[0]
    level = int(vars[1])
    candidates = vars[2:len(vars)]
    
    #entries = {cand:'' for cand in candidates}
    nltk.corpus.cmudict.entries()
    #for word in candidates:
        #entries[word] = nltk.corpus.cmudict.entries()[word] 
    
    #print str(rhyme(vars[0], vars[1:len(vars)], 1))
    print str(rhyme(target, candidates, level))