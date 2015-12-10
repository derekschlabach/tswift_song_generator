from nltk import FreqDist

#Taken from project 3
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
