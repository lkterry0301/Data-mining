import time
import json
import sys
import imp
import os
import random
import math
import json
lab2 = imp.load_source('lab2', os.getcwd()+"/../lab2/lab2.py")

#no longer TF-IDF values, just whether or not the word is in the hash
def vectorized_feature_vectors_indicating_word_presence():
    tfidf_larger,tfidf_smaller = lab2.get_feature_vectors()
    
    for doc in tfidf_smaller:
        for key in doc[1].keys():
            if doc[1][key] > 0:
                doc[1][key] = 1
    
    #vectorize    
    all_words = lab2.get_unique_words_in_tfidf_data(tfidf_smaller)
    all_class_labels = lab2.get_unique_class_labels_in_tfidf_data(tfidf_smaller)
    
    return lab2.get_training_samples_and_class_labels_vectors(tfidf_smaller, all_words, all_class_labels)

def main():
    print ""
    start_time = time.time()
    
    vectorized_data_words, vectorized_class_labels = vectorized_feature_vectors_indicating_word_presence()
    #print vectorized_data_words
    
    print "Total running time: "+str(time.time()  - start_time)+" seconds"
    print ""

#calls the main() function
if __name__ == "__main__":
    main()