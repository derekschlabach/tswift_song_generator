from custom.syll import syllables

while True :
    var = raw_input("Enter a word: ")
    print var + ": " + str(syllables(var))
