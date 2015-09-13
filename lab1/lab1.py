#!/usr/bin/env python

import sys
import os
import time
import string
import math
import nltk #natural language toolkit
from nltk import stem
from nltk.corpus import stopwords
from bs4 import BeautifulSoup #xml/html parser, will be used for sgml data files

#global variables
stemmer = stem.porter.PorterStemmer() #porter can be switched with lancaster or snowball for different stemming variants
cached_stop_words = stopwords.words("english") #caching stop words speeds it up a lot
cached_punctuation = string.punctuation
remove_punctuation_map = dict((ord(char), None) for char in cached_punctuation) #map string.punctuation values into Unicode. Use this as a mapping function to delete punctuation

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

def get_reduced_words_with_their_counts(text,overall_word_counts):
    words = nltk.word_tokenize(text.lower())
    words_with_count = dict([]);
    
    #iterate through the words and add to the word count if needed
    for word in words:
        if not should_filter_out_word(word):
            stemmed_word = stemmer.stem(word)
            
            if stemmed_word in words_with_count:
                words_with_count[stemmed_word] += 1
            else:
                words_with_count[stemmed_word] = 1
            
            if stemmed_word in overall_word_counts:
                overall_word_counts[stemmed_word] += 1
            else:
                overall_word_counts[stemmed_word] = 1                
            
    
    return words_with_count

def get_and_count_body_words(reuter,overall_word_counts):
    text_tag = reuter.find("text")
    body_text = text_tag.text
    
    return get_reduced_words_with_their_counts(body_text,overall_word_counts)

def get_class_label(reuter):
    reuter_text = reuter.find("text")
    
    #get relevant fields from the REUTERS tag
    topics = reuter.topics
    places = reuter.places
    title = reuter_text.title
    
    #init the class label dictionary
    class_label = dict([])
    class_label['topics'] = set()
    class_label['places'] = set()
    class_label['title'] = ""
    
    #iterate and add words to label
    if topics != None:
        for child in topics.children:
            class_label['topics'].add(child.text)
    if places != None:
        for child in places.children:
            class_label['places'].add(child.text)
    if title != None:
        class_label['title']=title.text
        
    return class_label

def term_frequency_filtering(data_matrix,overall_word_counts):
    print "before term freq "+str(len(overall_word_counts))
    for key in overall_word_counts.keys():
        if overall_word_counts[key] < 20:
            remove_word_from_data_matrix(key,data_matrix)
            del overall_word_counts[key]
    print "after term freq "+str(len(overall_word_counts))

def remove_word_from_data_matrix(word,data_matrix):
    data_matrix[0].remove(word)
    for i in range(1,len(data_matrix)): #iterate over all the documents in the data matrix
        if word in data_matrix[i][1]:
            del data_matrix[i][1][word]

"""
The data matrix format is as follows:
First row: The set of all interesting words in all the documents
Subsequent rows: A list of length 2 representing a reuters document. The 0 index is the class label, and the 1 index is a dictionary of words ('word': word_count). If the word is not in that dictionary, then it is not found in the document.
"""
def get_data_matrix(directory_with_files): 
    data_matrix = []
    data_matrix.append( set() ) #first row is a set of all words across all documents
    overall_word_counts = dict([]) #used to prevent having to reiterate over the data matrix a whole bunch for each term
    
    for filename in os.listdir(directory_with_files):
        current_data_file = open(directory_with_files+"/"+filename, "r")
        sgml_tree = get_parsed_document_tree(current_data_file)
        
        for reuter in sgml_tree.find_all("reuters"):       
            class_label = get_class_label(reuter)
            body_words_with_counts = get_and_count_body_words(reuter,overall_word_counts)
            
            #add document to data matrix
            data_matrix.append( [class_label,body_words_with_counts] )
            data_matrix[0].update( body_words_with_counts.keys() )
        
        current_data_file.close()
    
    term_frequency_filtering(data_matrix,overall_word_counts)
    
    return data_matrix

def main():
    start_time = time.time()
    data_matrix = get_data_matrix(os.getcwd()+"/../data_files")
    print("--- Program runs for %s seconds ---" % (time.time() - start_time))
    
    """
    i=0
    for row in data_matrix:
        print ""
        print row
        i+=1
        
        if i>3:
            break
    """
    
#calls the main() function
if __name__ == "__main__":
    main()
