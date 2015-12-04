import syll

while True :
    var = raw_input("Enter a word: ")
    print var + ": " + str(syll.numSyllables(var))
