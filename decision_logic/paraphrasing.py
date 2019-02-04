from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
import re
import string
from random import *
import pprint

#pass in string and return array of objects with each word in a tuple with its word type tag
def label_words(sentence):
    
    words = sentence.split(" ")
    punctuation_without_apostrophe = string.punctuation.replace("'", "")
    
    words_with_tokenised_punctuation = []
    
    for index, word in enumerate(words):
        
        if any((c in punctuation_without_apostrophe) for c in word):
            tokens = word_tokenize(word)
            for token in tokens:
                words_with_tokenised_punctuation.append(token)
        else:
            words_with_tokenised_punctuation.append(word)
    
    #eremove any empty strings
    for index, word in enumerate(words):
        if(len(word) == 0): 
            words.remove(index)
    
    words = pos_tag(words) #label each word in array with it word type tag 
    
    return words

#pass in word type tag to determine if word can be synonymised
def is_synonymisable(word, tag):
    #return tag == 'VB' or tag.startswith('JJ') #dont synonymise only verbs and adjectives
    return tag.startswith('NN') or tag == 'VB' or tag.startswith('JJ') #synonymise nouns, verbs and adjectives

#pass in word and its word type tag and get list of usable synonyms for the word
def synonyms(word, tag):
    lemma_lists = [ss.lemmas() for ss in wordnet.synsets(word, get_constant(tag))] #access list of raw synonyms using word type tag
    lemmas = [lemma.name() for lemma in sum(lemma_lists, [])] #root list of raw synonyms to get usable word
    return set(lemmas)

#get wordnet constant to make synonym more appropriate
def get_constant(tag):
    if tag.startswith('NN'):
        return wordnet.NOUN
    elif tag.startswith('V'):
        return wordnet.VERB

#pass in a sentence and find a list of synonyms for each word
def synonymIfExists(sentence):
    for (word, tag) in label_words(sentence):
        if is_synonymisable(word, tag):
            syns = synonyms(word, tag) #get synonyms for word based on word type tag
            if syns:
                if len(syns) > 1:
                    yield [word, list(syns)]
                    continue
        yield [word, []]

def paraphrase(sentence):
    
    output_sentence = ""
    
    words_with_synonyms = [x for x in synonymIfExists(sentence)]
    
    for word, synonyms in words_with_synonyms:
        if len(synonyms) > 0:
            #print(synonyms)
            ran = randint(0, len(synonyms) - 1)
            #print(ran)
            output_sentence += synonyms[ran].replace("_", " ") + " "
        else:
            output_sentence += word + " "
            
    return output_sentence

#input_string = "I can't and won't do this later, ok buddy? yes."
input_string = """The brief introduction summarizes the song's satirical message: that Eminem is the lead "singer" of the "band" and it makes everyone else in D12 jealous and looked down upon. In the chorus, he describes how girls have confidence in the group just because he is in it, even though they “don’t even know the name of [his] band”.Eminem talks about his own popularity in the first verse and the conflict it creates within the group. He describes episodes such as female fans attempting to make sexual advances when meeting him offstage, and group member Kuniva trying to attack him with a knife when he claims that Jessica Alba is his "wife-to-be"."""

#print(input_string)

#print(paraphrase(input_string))