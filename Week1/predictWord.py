from nltk.corpus import abc
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import re

def predict(string):
    # pre-processing starts here
    quotes_token = word_tokenize(string)
    
    punctuation = re.compile(r'[-.?!.:;()|0=9]')
    post_punctuation = []
    for words in quotes_token:
        word = punctuation.sub("", words)
        if len(word) > 0:
            post_punctuation.append(word)
        
    word_tuple = tuple(post_punctuation)
    
    words = abc.words('science.txt')
    words_as_ngrams = list(ngrams(words, len(word_tuple)+1))
    
    acquired = []
    index = 0
    for element in word_tuple:
        if len(acquired) == 0:
            to_iterate = words_as_ngrams
        else:
            to_iterate = acquired
            acquired = []
        for x in to_iterate:
            word = x[index]
            if word == element:
                acquired.append(x)
        index += 1
    
    distinct_count = {}
    for element in acquired:
        word = element[len(element)-1]
        if word not in distinct_count:
            distinct_count[str.lower(element[len(element)-1])] = 1
    
    for element in acquired:
        distinct_count[str.lower(element[len(element)-1])] += 1
            
    return distinct_count