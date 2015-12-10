#author Derek Schlabach
from custom.functions import *

while True :
    var = raw_input("Enter a word: ")
    print var + ": " + str(syllables(var))
