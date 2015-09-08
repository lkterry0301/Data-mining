#!/usr/bin/env python

import sys
import os
import time
import string
import nltk #natural language toolkit
from nltk import stem
from nltk.corpus import stopwords
from bs4 import BeautifulSoup #xml/html parser, will be used for sgml data files

#global variables
stemmer = stem.porter.PorterStemmer() #porter can be switched with lancaster or snowball for different stemming variants
cached_stop_words = stopwords.words("english") #caching stop words speeds it up a lot
cached_punctuation = string.punctuation
remove_punctuation_map = dict((ord(char), None) for char in cached_punctuation) #map string.punctuation values into Unicode. Use this as a mapping function to delete punctuation
frequency_trimming_threshold = .01

def get_parsed_document_tree(data_file):
    #Use the BeautifulSoup Library to create a Parse Tree out of the text
    all_document_text =  data_file.read()
    tree = BeautifulSoup(all_document_text,'lxml')
    return tree

def should_filter_out_word(word):
    word_without_punc = word.translate(remove_punctuation_map)#remove any punctuation characters and save to temp variable. This will ensure strings like "...","'s","--",etc are removed but strings like "O'Reilly" are preserved with punctuation
    try:
        #remove integers, floats, or any kind of number. A date '9/12/2012' will be transformed to 9122012 and thus removed.
        float(word_without_punc)
        return True
    except ValueError:#not a number, check other cases and perform necessary translations (like stemming) on the word
        #After removing punctuation, "..." maps to "", "'s" maps to "s" 
        #Remove these cases and any other 0 or 1 character cases, of which there are no interesting English words
        #Also, remove stop words
        if len(word_without_punc) < 2 or word_without_punc in cached_stop_words:
            return True
        else:
           return False

def get_word_list_and_reduce(text):
    words = nltk.word_tokenize(text.lower())
    
    #iterate through the words and check for special cases
    for i in range(len(words)-1,-1,-1):
        if should_filter_out_word(words[i]):
            del words[i]
        else:
            words[i] = stemmer.stem(words[i])
    
    return words

def get_body_words(reuter):
    text_tag = reuter.find("text")
    body_text = text_tag.text
    
    return get_word_list_and_reduce(body_text)

def count_words(word_list,dictionary):
    for word in word_list:
        if dictionary.get(word) == None:
            dictionary[word] = 1
        else:
            dictionary[word] += 1

"""
def trim_words_based_upon_overall_frequency(data_matrix):
    overall_max = -1 * sys.maxint
    for column in data_matrix:
        column_max = max(column)
        if column_max > overall_max
            overall_max = column_max
    
    for column in data_matrix:
        max_column_value = max(column)
        if max_column_value < 4 or max_column_value > 0.99 * overall_max:
            del data_matrix.column
"""

def print_data(dictionary):
    for key,value in dictionary.iteritems():
        print "    "+key+": "+str(value)

def add_to_class_label(reuter,dictionary):
    reuter_text = reuter.find("text")
    #get relevant fields from the REUTERS tag
    topics = reuter.topics
    places = reuter.places
    title = reuter_text.title
    
    #iterate and add words to label
    if topics != None:
        for child in topics.children:
            dictionary['topics'].add(child.text)
    if places != None:
        for child in places.children:
            dictionary['places'].add(child.text)
    if title != None:
        dictionary['title']=title.text
    
def init_transaction_data():
    transaction_data = {'class_label': dict([]),'body':dict([])}  
    #initialize the three fields of the class label
    transaction_data['class_label']['topics'] = set()
    transaction_data['class_label']['places'] = set()
    transaction_data['class_label']['title'] = ""
    return transaction_data
    
def get_transaction_data(directory_with_files): 
    all_transaction_data = []
    for filename in os.listdir(directory_with_files):
        current_data_file = open(directory_with_files+"/"+filename, "r")
        sgml_tree = get_parsed_document_tree(current_data_file)
        
        for reuter in sgml_tree.find_all("reuters"):    
            transaction_data = init_transaction_data()
            
            add_to_class_label(reuter,transaction_data['class_label'])
            
            #parse body into relevant word tokens
            body_words = get_body_words(reuter)
            count_words(body_words,transaction_data['body'])
            
            if len(transaction_data['body'].keys()) == 0:
                transaction_data['body']['arbitrary_key_to_make_non_empty'] = 1
            
            all_transaction_data.append(transaction_data)
        
        current_data_file.close()
    return all_transaction_data

def main():
    start_time = time.time()
    all_transaction_data = get_transaction_data(os.getcwd()+"/../data_files")
    print("--- Program runs for %s seconds ---" % (time.time() - start_time))
    
    for transaction_data in all_transaction_data:
        print ""
        print_data(transaction_data['class_label'])
        print_data(transaction_data['body'])
    
#calls the main() function
if __name__ == "__main__":
    main()
