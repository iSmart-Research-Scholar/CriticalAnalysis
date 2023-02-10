import nltk
nltk.download('stopwords')
from nltk import bigrams
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.corpus import stopwords

class CriticalAnalysis:
    def Score(listIs):
            initial = ""

            for paper in listIs:
                if paper['abstract'] != None:
                    initial += paper['abstract']

                    initial = initial.lower()
                    initial = initial.replace('-', '')
                    initial = initial.replace('.', '')
                    initial = initial.replace(',', '')

                    # Prepare the text data
                    
            word_tokens = initial.split(' ')

            stop_words = set(stopwords.words('english'))

            filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

            text = ' '.join(filtered_sentence)
            # Convert the text into a list of words
            words = nltk.word_tokenize(text)

            # Generate the bigrams from the words
            bigram_list = list(bigrams(words))

            # Create a frequency distribution of the bigrams
            bigram_freq = FreqDist(bigram_list)

            # Create a conditional frequency distribution of the bigrams
            bigram_cond_freq = ConditionalFreqDist([(w1, w2) for w1, w2 in bigram_list])

            # Calculate the probability of a word giv0en its previous word
            listIs = text.split(' ')
            dict_prob = {}
            for i in range(len(listIs)-1):
                if(text.count(listIs[i]) > 6 and len(listIs[i]) > 3 and bigram_cond_freq[listIs[i]].freq(listIs[i+1]) != 1):
                    dict_prob[f"{listIs[i]} {listIs[i+1]}"] = bigram_cond_freq[listIs[i]].freq(listIs[i+1])

            dict_prob = list(sorted(dict_prob.items(), key = lambda kv: (kv[1]), reverse=True))
            listIs = []
            for i in range(10):
                listIs.append(dict_prob[i][0])
            return {"queryparams": listIs}
