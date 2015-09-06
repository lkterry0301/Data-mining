#!/usr/bin/env python

import sys
import os
import nltk #natural language toolkit
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
    return BeautifulSoup(parsable_text,'xml')

def main():
    for filename in os.listdir(os.getcwd()+"/../data_files"):
        current_data_file = open("../data_files/"+filename, "r")
        
        sgml_tree = get_parsed_document_tree(current_data_file)
        #print sgml_tree.prettify() #ensure that the document tree is working
        
        current_data_file.close()

#calls the main() function
if __name__ == "__main__":
    main()
