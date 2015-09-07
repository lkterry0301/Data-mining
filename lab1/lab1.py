#!/usr/bin/env python

import sys
import os
import string
import nltk #natural language toolkit
from nltk import stem
from bs4 import BeautifulSoup #xml/html parser, will be used for sgml data files

def transform_document_text_for_parsing(all_document_text):
    #Parsers assume the document has a wrapper tag. The provided data files do not. So add one in after the Doctype declaration and close it at the end of the file.
    oldBeginning = "<!DOCTYPE lewis SYSTEM \"lewis.dtd\">"
    newBeginning = "<!DOCTYPE lewis SYSTEM \"lewis.dtd\"><TOTAL_DOCUMENT_WRAPPER_TAG_FOR_PARSING>" #add the tag after DocType
    new_doc_text = all_document_text.replace(oldBeginning,newBeginning,1)#replace the initial (and only) docType
    new_doc_text = new_doc_text + "</TOTAL_DOCUMENT_WRAPPER_TAG_FOR_PARSING>"#close new tag at end of text
    return new_doc_text

def get_parsed_document_tree(data_file):
    #Use the BeautifulSoup Library to create a Parse Tree out of the text
    all_document_text =  data_file.read()
    parsable_text = transform_document_text_for_parsing(all_document_text)
    tree = BeautifulSoup(parsable_text,'xml')#NOTE: this is an xml parse for an sgml data file. This may cause issues but appears to be working fine
    return tree

def get_word_list_and_reduce(text):
    words = nltk.word_tokenize(text.lower())
    stemmer = stem.porter.PorterStemmer() #porter can be switched with lancaster or snowball for different stemming variants
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation) #map string.punctuation values into Unicode. Use this as a mapping function to delete punctuation
    
    #iterate through the words and check for special cases
    for i in range(len(words)-1,-1,-1):
        word = words[i].translate(remove_punctuation_map)#remove any punctuation characters and save to temp variable. This will ensure strings like "...","'s","--",etc are removed but strings like "O'Reilly" are preserved with punctuation
        try:
            #remove integers, floats, or any kind of number. A date '9/12/2012' will be transformed to 9122012 and thus removed.
            float(word)
            del words[i]
        except ValueError:#not a number, check other cases and perform necessary translations (like stemming) on the word
            #After removing punctuation, "..." maps to "", "'s" maps to "s", and "n't" maps to "nt". 
            #Remove these cases and any other 0, 1, or 2 character cases, of which there are no viable English words (other than 'I' and 'A', which are not interesting here).
            #Also, remove stop words
            if len(word) <= 2 or word in nltk.corpus.stopwords.words('english'):
                del words[i]
            else:
                words[i] = stemmer.stem(words[i])
    
    return words

def get_body_words(reuter):
    body_text = ""
    text_tag = reuter.find("TEXT")
    #handle bad formatting where BODY tag was not included
    if text_tag.BODY != None:
        body_text = text_tag.BODY.text
    else:
        body_text = text_tag.text
    
    return get_word_list_and_reduce(body_text)

def count_words(word_list,dictionary):
    for word in word_list:
        if dictionary.get(word) == None:
            dictionary[word] = 1
        else:
            dictionary[word] += 1
    
def trim_words_based_upon_frequency(dictionary):    
    #print "Before frequency based trimming "
    #print "There are "+str(len(dictionary))+" unique words"
    #print "The minimum is: "+str(min(dictionary.values()) )
    #print "The maximum is: "+str(max(dictionary.values()) )
    
    max_val = max(dictionary.values())
    threshold = .01
    
    for key in dictionary.keys():
        #remove extremely frequent words
        if dictionary[key] > (max_val - max_val*threshold):
            del dictionary[key]
            
        #remove extremely infrequent words
        elif dictionary[key] < (max_val*threshold):
            del dictionary[key]
            
    
    #print "After frequency based trimming "
    #print "There are "+str(len(dictionary))+" unique words"
    #print "The minimum is: "+str(min(dictionary.values()) )
    #print "The maximum is: "+str(max(dictionary.values()) )

def print_data(filename,dictionary):
    print filename
    for key,value in dictionary.iteritems():
        print "    "+key+" "+str(value)



def add_to_class_label(reuter,dictionary):
    #get relevant fields from the REUTERS tag
    topics = reuter.TOPICS
    places = reuter.PLACES
    title = reuter.find("TEXT").TITLE
    
    #iterate and add words to label
    for child in topics.children:
        dictionary['topics'].append(child.text)
    for child in places.children:
        dictionary['places'].append(child.text)
    if title != None:
        dictionary['titles'].append(title.text)
    
def init_transaction_data():
    transaction_data = {'class_label': dict([]),'body':dict([])}  
    #initialize the three fields of the class label
    transaction_data['class_label']['topics'] = []
    transaction_data['class_label']['places'] = []
    transaction_data['class_label']['titles'] = []  
    return transaction_data
    
def main():   
    for filename in os.listdir(os.getcwd()+"/../data_files"):
        current_data_file = open("../data_files/"+filename, "r")
        sgml_tree = get_parsed_document_tree(current_data_file)    
        transaction_data = init_transaction_data()
        
        for reuter in sgml_tree.find_all("REUTERS"):
            add_to_class_label(reuter,transaction_data['class_label'])
            
            #parse body into relevant word tokens
            body_words = get_body_words(reuter)
            count_words(body_words,transaction_data['body'])
        
        
        trim_words_based_upon_frequency(transaction_data['body'])
        #print_data(filename,transaction_data['class_label'])
        #print_data(filename,transaction_data['body'])
        
        current_data_file.close()
    

#calls the main() function
if __name__ == "__main__":
    main()
