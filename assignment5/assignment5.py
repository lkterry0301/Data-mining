import time
import json
import sys
import imp
import os
import random
import math
import json
lab2 = imp.load_source('lab2', os.getcwd()+"/../lab2/lab2.py")

true_similarity_file = os.getcwd()+"/../feature_vectors/true_jaccard_similarity.dat"

# Copied from http://stackoverflow.com/a/15862048
def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "="*block + " "*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def hash_document(doc,a,b,):
    return

def jaccard_similarity_of_bit_vectors(bv1,bv2):
    if(bv1 or bv2 == 0):
        return 0
    else:
        return ((bv1 and bv2) + 0.0) / (bv1 or bv2)

def jaccard_similarity(vector1,vector2):
    #the vectors are both a list of 0 and 1 where 1 indicates a word is present in this vectorized document in the article.
    #Thus, a 0 indicates a word is missing from the doc's vector. This indicates it should not be counted in the Jaccard similarity
    intersect_size = 0
    vec1_size = 0
    vec2_size = 1
    
    for i in range(0,len(vector1)):
        vec1_size += vector1[i] + 0.0
        vec2_size += vector2[i] + 0.0
        intersect_size += (vector1[i] and vector2[i]) + 0.0
    
    jaccard_val = intersect_size / (vec1_size + vec2_size - intersect_size)
    return jaccard_val

def baseline_similarity(vectorized_data_words, force_recalculate=False):
    #check to see if baseline has already been calculated in a previous run. Load and return it if it has
    if os.path.exists(true_similarity_file) and not force_recalculate: 
        print "Using True Similarity calculations from a previous run of this lab. Loading JSON..."
        sim_file = open(true_similarity_file, "r")
        return json.loads( sim_file.read() )
    
    print "Finding True similarity between every document pair. Started at: "+ str(time.ctime(int(time.time())))
    
    true_similarity = list()
    run_time_complexity = len(vectorized_data_words) * len(vectorized_data_words) + 0.0 #(len(vectorized_data_words) * (len(vectorized_data_words)+1))  / (2+0.0)
    
    #compare each file to every other file
    for i in range(0,len(vectorized_data_words)):
        next_row = list()
        
        #speed it up a bit by realizing many comparisons will already have been made at later iterations
        if i>0:
            for j in range(0,i):
                next_row.append(true_similarity[i-1][j])
                
                progress_in_percent = ( i * len(vectorized_data_words) + j) / run_time_complexity
                update_progress( progress_in_percent ) 
        
        next_row.append(1) #Jaccard imilarity to itself is 1
        
        for j in range (i+1,len(vectorized_data_words)):
            v1 = vectorized_data_words[i]
            v2 = vectorized_data_words[j]
            next_row.append(jaccard_similarity_of_bit_vectors(v1,v2)) 
            
            progress_in_percent = ( i * len(vectorized_data_words) + j) / run_time_complexity
            update_progress( progress_in_percent ) 
        
        true_similarity.append(next_row)
    
    
    sim_file = open(true_similarity_file,'w')
    json.dumps(true_similarity, sim_file)
    
    return true_similarity

def bit_vector_from_word_vector(word_v):
    word_v_as_str = "".join(map(str, word_v))
    return int(word_v_as_str,base = 2)

#no longer TF-IDF values, just whether or not the word is in the hash
def vectorized_feature_vectors_indicating_word_presence():
    tfidf_larger,tfidf_smaller = lab2.get_feature_vectors()
    
    #convert tfidf values to booleans
    for doc in tfidf_smaller:
        for key in doc[1].keys():
            if doc[1][key] > 0:
                doc[1][key] = 1
    
    #vectorize    
    all_words = lab2.get_unique_words_in_tfidf_data(tfidf_smaller)
    all_class_labels = lab2.get_unique_class_labels_in_tfidf_data(tfidf_smaller)
    
    vectorized_data_words, vectorized_class_labels = lab2.get_training_samples_and_class_labels_vectors(tfidf_smaller, all_words, all_class_labels)
    
    #convert boolean lists to bit vectors
    for i in range(0, len(vectorized_data_words)):
        vectorized_data_words[i] = bit_vector_from_word_vector(vectorized_data_words[i])
    
    return vectorized_data_words, all_words

def main():
    print ""
    start_time = time.time()
    
    vectorized_data_words, word_ordering  = vectorized_feature_vectors_indicating_word_presence()
    
    baseline_similarity(vectorized_data_words)
    
    print "Total running time: "+str(time.time()  - start_time)+" seconds"
    print ""

#calls the main() function
if __name__ == "__main__":
    main()