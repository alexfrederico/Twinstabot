import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
from nltk import FreqDist
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def analyze_feeling(text):
    sentiment = ""
    phrase_pt = ''
    phrase_en = ''
    phrase = ''
    try:
        phrase_pt = TextBlob(text, analyzer=NaiveBayesAnalyzer())
        phrase_en = phrase_pt.translate(from_lang='pt',to='en')
        phrase = TextBlob(str(phrase_en), analyzer=NaiveBayesAnalyzer())
        print(phrase_pt)
        print(phrase.sentiment[0])
        print()
        sentiment = "neu" if phrase.sentiment[1] == phrase.sentiment[2] else phrase.sentiment[0]
    except Exception as error:
        print('analyze_feeling - ',phrase_pt,' - ',phrase,' - ',error)
        sentiment = "Not identified"
    return sentiment

def create_most_frequent_words(filtered_word_list,max_words):
    most_frequent_words = FreqDist(filtered_word_list).most_common(max_words)
    single_words = []
    for i in most_frequent_words:
        single_words += [i[0]]
    return single_words

def create_trigrams(word_list,prepositions,max_trigrams,min_freq_appearances=3):
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = nltk.collocations.TrigramCollocationFinder.from_words(word_list)
    finder.apply_freq_filter(min_freq_appearances)
    trigram_words = set()
    for i in finder.score_ngrams(trigram_measures.likelihood_ratio):
        if len(trigram_words) == (max_trigrams):
            break
        if i[0][0] in prepositions or i[0][2] in prepositions:
            continue
        trigram_words.add(i[0][0]+i[0][1]+i[0][2])
    return list(trigram_words)

def create_bigrams(word_list,prepositions,max_bigrams,min_freq_appearances=3):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = nltk.collocations.BigramCollocationFinder.from_words(word_list)
    finder.apply_freq_filter(min_freq_appearances)
    bigram_words = set()
    for i in finder.score_ngrams(bigram_measures.likelihood_ratio):
        if len(bigram_words) == max_bigrams:
            break
        if i[0][0] in prepositions or i[0][1] in prepositions:
            continue
        bigram_words.add(i[0][0]+i[0][1])
    return list(bigram_words)

def create_hashtags(texts,filtered_texts,max_single_words=5,max_two_words=5,max_three_words=5):
    prepositions = ['a', 'o', 'ao', 'aos', 'que', 'ante', 'após', 'até', 'com', 'contra', 'da', 'de', 'do', 'das', 'dos', 'desde', 'em', 'entre', 'para', 'per', 'perante', 'por', 'sem', 'sob', 'sobre', 'trás','foi']
    word_list = ' '.join(texts).split()
    filtered_word_list = ' '.join(filtered_texts).split()
    hashtags = []
    hashtags += create_most_frequent_words(filtered_word_list,max_single_words)
    hashtags += create_bigrams(word_list,prepositions,max_two_words)
    hashtags += create_trigrams(word_list,prepositions,max_three_words)
    return '#'+(' #'.join(hashtags))

def remove_stop_words(text,stopwords):
    new_text = []
    for word in text.split():
        if word not in stopwords:
            new_text += [word]
    return ' '.join(new_text)

def create_stopwords():
    stopwords_nlkt = set(nltk.corpus.stopwords.words('portuguese'))
    additional_stopwords = set(open('.\docs\stopwords.txt', encoding='utf-8').read().split('\n'))
    combined_stopwords =  stopwords_nlkt.union(additional_stopwords)
    return list(combined_stopwords)

def regex_word_removal(text):
    filtered_text = text.lower()
    filtered_text = re.sub(r'(http|https)[^ ]* ','', filtered_text) #Remove links
    filtered_text = re.sub(r'[^a-z]k+[^a-z]',' ', filtered_text) #Removes onomatopoeia (laughs)
    filtered_text = re.sub(r'[^a-z 0-9áéíóúâêîôãõçàûü]',' ', filtered_text) #remove special characters
    for letter in 'abcdefghijklmnopqrstuvwxyzáãâàçéêíîóôõúûü ': #Removes excessively inserted letters
        filtered_text = re.sub(r''+letter+'('+letter+'+)',letter+letter, filtered_text) 
    filtered_text = re.sub(r' (a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|á|ã|â|à|ç|é|ê|í|î|ó|ô|õ|ú|û|ü) ',' ', filtered_text) #removes words with a single character
    return filtered_text
