#!/usr/bin/env python

import sys
import os
import nltk #natural language toolkit
from nltk import stem
from bs4 import BeautifulSoup #xml/html parser, will be used for sgml data files

def transform_document_text_for_parsing(all_document_text):
    #Parsers assume the document has a wrapper. The provided data files do not. So add one in after the Doctype declaration and close it at the end of the file.
    oldBeginning = "<!DOCTYPE lewis SYSTEM \"lewis.dtd\">"
    newBeginning = "<!DOCTYPE lewis SYSTEM \"lewis.dtd\"><TOTAL_DOCUMENT_WRAPPER_TAG_FOR_PARSING>" #add the tag after DocType
    new_doc_text = all_document_text.replace(oldBeginning,newBeginning,1)#replace the initial (and only) docType
    new_doc_text = new_doc_text + "</TOTAL_DOCUMENT_WRAPPER_TAG_FOR_PARSING>"#close new tag
    return new_doc_text

def get_parsed_document_tree(data_file):
    #Use BeautifulSoup Library to create a Parse Tree out of the text
    all_document_text =  data_file.read()
    parsable_text = transform_document_text_for_parsing(all_document_text)
    tree = BeautifulSoup(parsable_text,'xml')
    return tree

def get_word_list(text):
    words = nltk.word_tokenize(text.lower())
    
    #remove stop words via a set difference
    words = list(set(words) - set(nltk.corpus.stopwords.words('english')) )
    
    #stem evey word
    stemmer = stem.porter.PorterStemmer() #porter can be switched with lancaster or snowball for different stemming variants
    for i in range(0,len(words)):
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
    
    return get_word_list(body_text)

def main():
    for filename in os.listdir(os.getcwd()+"/../data_files"):
        current_data_file = open("../data_files/"+filename, "r")
        sgml_tree = get_parsed_document_tree(current_data_file)       
        
        for reuter in sgml_tree.find_all("REUTERS"):
            #get relevant fields from the REUTERS tag
            topics = reuter.TOPICS
            places = reuter.PLACES
            title = reuter.find("TEXT").TITLE
            
            #parse body into relevant tokens
            body_words = get_body_words(reuter)
        
        current_data_file.close()

#calls the main() function
if __name__ == "__main__":
    main()
