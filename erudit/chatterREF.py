import os
import ast
import random
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import re
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
#nltk.download('popular', quiet=True)
# nltk.download('punkt') # first-time use only
# nltk.download('wordnet') # first-time use only

THIS_FOLDER1 = os.path.dirname(os.path.abspath(__file__))
my_file1 = os.path.join(THIS_FOLDER1, 'refbot.txt')
# Reading in the corpus
with open(my_file1, 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()
THIS_FOLDER2 = os.path.dirname(os.path.abspath(__file__))
my_file2 = os.path.join(THIS_FOLDER2, 'referinte.txt')
with open(my_file2, 'r', encoding='utf8', errors='ignore') as fin2:
    token_prop = fin2.read().lower().split("\n")
#print(token_prop)
# Tokenisation
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words
#print(sent_tokens)
#token_prop = nltk.sent_tokenize(refs)
#print(token_prop)
# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
# Keyword Matching
GREETING_INPUTS = ("hey", "ciao", "hi", "yo", "hello", "good day")
GREETING_RESPONSES = ["Hi", "Hey", "Yo", "Greetings", "Nice to meet you! You are talking with me", "Hello"]
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + ".</br>" + "Please, type a word, syntagm or sentence (e.g. ai, transparency)."

def response(user_response):
    gigr = greeting(user_response)
    robo_response = ''
    verif = 0
    for i in sent_tokens:
        #print(i)
        if user_response.lower() == i:
            verif = 1
            #print("Aicia l-am prins, bai!")
    if verif==0:
        sent_tokens.append(user_response.lower())
    #print(sent_tokens)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
    #print(TfidfVec)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    #print(tfidf)
    #print(type(tfidf))
    vals = cosine_similarity(tfidf[-1], tfidf)
    #print(vals)
    idx = vals.argsort()[0][-2]
    #print(vals.argsort())
    #print(idx)
    rezolvare = vals.argsort().flatten()
    #el = rezolvare[-2]
    for i in range(len(rezolvare)):
        raspu = i + 1
    flat = vals.flatten()
    # print(flat)
    flat.sort()
    # print(flat)
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        if gigr != None:
            return gigr
        else:
            robo_response = robo_response + "Sorry, I don't understand."
            return robo_response
    else:
        extragere = re.findall(r'\[\d+\]', sent_tokens[idx])
        print(extragere)

        if extragere != []:
            x = ast.literal_eval(extragere[0])
            #print(x)
        if extragere == []:
            robo_response = robo_response + sent_tokens[idx] + "; Without reference. \
                             Please, try with a new word, syntagm or sentence."
            return robo_response

        nrref = x[0]
        for i in range(len(token_prop) + 1):
            if int(nrref) == i + 1:
                robo_response = robo_response + sent_tokens[idx] + "</br>" + "Associated reference: " + token_prop[i]
        # robo_response = robo_response+sent_tokens[idx]+"\n"+token_prop[el]
        return robo_response