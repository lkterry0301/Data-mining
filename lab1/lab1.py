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
num_words_in_tf_idf_filter = 500
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
    try:
        #remove integers, floats, or any kind of number. A date '9/12/2012' will be transformed to 9122012 and thus removed.
        int(word)
        return True
    except ValueError:#not a number, check other cases and perform necessary translations (like stemming) on the word
        #After removing punctuation, "..." maps to "", "'s" maps to "s" 
        #Remove these cases and any other 0 or 1 character cases, of which there are no interesting English words
        #Also, remove stop words
        if len(word) < 2 or word in cached_stop_words:
            return True
        else:
           return False

def increment_hash(dictionary,key):
    dictionary[key] = dictionary.get(key,0) + 1

def sorted_dict_as_list(d):
    return sorted(d.iteritems(),key=lambda(k,v):(v,k))
    
def process_words(reuter, doc_counts):
    #parse the reuter tag
    text_tag = reuter.find("text")
    body_text = text_tag.text
    
    words = nltk.word_tokenize(body_text.lower())
    words_with_count = dict([]);
    
    #iterate through the words and add to the word count if needed
    for i in range(len(words)-1, -1,-1):    
        words[i] = words[i].translate(remove_punctuation_map)
        
        if not should_filter_out_word(words[i]):
            stemmed_word = stemmer.stem(words[i])
            increment_hash(words_with_count,stemmed_word)
    
    for word in words_with_count:
        increment_hash(doc_counts,word)
    
    return words_with_count

def document_frequency_filtering(data_matrix,doc_counts):
    words_to_remove = set()
    upper_remove_threshold_for_document_freq = (len(data_matrix) - 1) * .99
    lower_remove_threshold_for_document_freq = (len(data_matrix) - 1) * .01

    for key in doc_counts.keys():
        if doc_counts[key] > upper_remove_threshold_for_document_freq:
            words_to_remove.add(key)
        elif doc_counts[key] < lower_remove_threshold_for_document_freq:
            words_to_remove.add(key)
    
    remove_words_from_data_matrix(words_to_remove,data_matrix)

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

def get_tf_idf(data_matrix,doc_counts):
    overall_tf_idf = dict([])
    
    num_docs = len(data_matrix)-1
    for i in range(1,len(data_matrix)):
        tf_idf = dict([])
        
        for word in data_matrix[i][1]:
            tf_idf[word] = data_matrix[i][1][word] * math.log( num_docs/doc_counts[word] )
        
        tf_idf_sorted = sorted_dict_as_list(tf_idf)
        for i in range(0, min(15,len(tf_idf_sorted)) ):
            overall_tf_idf[ tf_idf_sorted[i][0] ] = tf_idf_sorted[i][1]
   
   
    best_overall_tf_idf_list = sorted_dict_as_list(overall_tf_idf)
    overall_tf_idf = dict([]) #reset the hash so that only the very best are included
    
    #make the list a hash
    for pair in best_overall_tf_idf_list:
        overall_tf_idf[ pair[0] ] = pair[1] 
    
    return overall_tf_idf

def remove_words_from_data_matrix(words,data_matrix):
    data_matrix[0] = data_matrix[0] - words
    for i in range(1,len(data_matrix)):
        for word in words:
            if word in data_matrix[i][1]:
                del data_matrix[i][1][word]

"""
The data matrix format is as follows:
First row: The set of all interesting words in all the documents
Subsequent rows: A list of length 2 representing a reuters document. The 0 index is the class label, and the 1 index is a dictionary of words ('word': word_count). If the word is not in that dictionary, then it is not found in the document.
"""
def get_feature_vectors(directory_with_files): 
    data_matrix = []
    data_matrix.append( set() ) #first row is a set of all words across all documents
    num_documents_words_occur_in = dict([])
    
    for filename in os.listdir(directory_with_files):
        current_data_file = open(directory_with_files+"/"+filename, "r")
        sgml_tree = get_parsed_document_tree(current_data_file)
        
        for reuter in sgml_tree.find_all("reuters"):       
            class_label = get_class_label(reuter)
            body_words_with_counts = process_words(reuter,num_documents_words_occur_in)
            
            #add document to data matrix
            data_matrix.append( [class_label,body_words_with_counts] )
            data_matrix[0].update( body_words_with_counts.keys() )
        
        current_data_file.close()
    
    tf_idf = get_tf_idf(data_matrix,num_documents_words_occur_in)
    document_frequency_filtering(data_matrix,num_documents_words_occur_in)
    
    return [tf_idf,data_matrix]

def main():
    start_time = time.time()
    feature_vectors = get_feature_vectors(os.getcwd()+"/../data_files")
    print("--- Feature vector creation/word extraction runs for %s seconds ---" % (time.time() - start_time))
    print ""
    
    print feature_vectors[0]
    
    for i in range(0,50): #visual seperation
        print ""
    
    matrix = feature_vectors[1]
    print matrix[0] #set of all unique words
    print ""
    for document_index in range(1,len(matrix)):
        print matrix[document_index][0]
        print matrix[document_index][1]
        print ""
    
#calls the main() function
if __name__ == "__main__":
    main()
