import time
import json
import sys
import imp
import os
import random
import math
import json
lab2 = imp.load_source('lab2', os.getcwd()+"/../lab2/lab2.py")
lab4 = imp.load_source('lab4', os.getcwd()+"/../assignment4/assignment4.py")

primes_under_1k = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

#true_similarity_file = os.getcwd()+"/../feature_vectors/true_jaccard_similarity.dat"

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
    text = "\rPercent: [{0}] {1}% {2}".format( "="*block + " "*(barLength-block), "{:.2f}".format(progress*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()


def doc_signature(doc,hash_functions_coefficients, prime):
    signature = list()
    
    for coeff in hash_functions_coefficients:
        hash_val = ( ( coeff[0] * doc + coeff[1] ) % prime ) % len(hash_functions_coefficients)
        signature.append(hash_val)
    
    return signature

"""
Converting sigantures to bit vectors is a little tricky. The signature is an ordered list of numbers representing hash bucket values. Every document has a signature of length num_hash_functions. In order for bitwise comparisons to be accurate, each value in the signature list must be converted to its binary representation and appended to a string. Finally the string is parsed into base 2.
ex: 4 hash functions
signature A = [0, 1, 1, 3] = 000 001 001 011 
signature B = [3, 1, 1, 0] = 011 001 001 000
Similarity (A,B): (A & B) / (A | B) = 2 / 6 = .33 
"""
def convert_signature_list_to_bit_vector(signature, num_hash_functions):
    binary_signature = ""
    
    for sig_val in signature:
        which_hash_bucket_is_filled = [0] * num_hash_functions
        which_hash_bucket_is_filled[sig_val] = 1 
        binary_signature += "".join(map(str, which_hash_bucket_is_filled)) #join list into string
    
    return int(binary_signature, base = 2)

def create_hash_signatures(vectorized_data_words,num_hash_functions):
    print "Creating document signatures..."
    start_time = time.time()
    
    all_doc_signatures = list()
    hash_coefficients, prime = create_hash_function_coefficients(num_hash_functions)
    
    for doc_bit_vector in vectorized_data_words:
        signature = doc_signature(doc_bit_vector,hash_coefficients, prime)
        signature_bit_vector = convert_signature_list_to_bit_vector(signature, num_hash_functions  ) 
        
        #all_doc_signatures.append( signature )
        all_doc_signatures.append( signature_bit_vector )
    
    print "It took "+str(time.time() - start_time)+"seconds to create document signatures with "+str(num_hash_functions)+" hash functions"
    return all_doc_signatures

#Mean Squared Error
def hash_similarity_MSE(true_similarity, hash_similarity):
    print "Calculating signature estimation Mean Squared Error..."
    mse = 0
    
    for i in range(0,len(true_similarity)): # len(true_similarity) == len(hash_similarity)
        for j in range(0, len(true_similarity[i]) ):# len(true_similarity[i]) == len(hash_similarity[i])
            mse += pow(true_similarity[i][j] - hash_similarity[i][j],2)
    
    return mse / len(true_similarity)

"""
Using Approximate Linear Hashing, a number of desired hash functions is given and they are constructed via 
h(x) = ((a*x+b) % P ) % N), where 
N is the number of hash functions, p is a prime greater than N, and
It appears that A is in the range [1, prime-1] and B is in the range [0,prime-1] --> https://www.cs.berkeley.edu/~daw/teaching/cs170-s03/Notes/lecture9.pdf
"""
def create_hash_function_coefficients(num_functions):
    hash_functions_coefficients = list()
    p = next_biggest_prime( num_functions )
    
    for i in range(0,num_functions):
        hash_functions_coefficients.append([random.randrange(1,p),random.randrange(0,p)])
    
    return hash_functions_coefficients, p

def jaccard_similarity_of_bit_vectors(bv1,bv2):
    or_val = bv1 | bv2
    if(or_val == 0):
        return 1
    else:
        return (bv1 and bv2 + 0.0) / (or_val)

def jaccard_similarity_of_signatures(s1,s2):
    intersect_size = 0
    
    for i in range(0,len(s1)):
        if(s1[i] == s2[i]):
            intersect_size += 1
    
    return (intersect_size+0.0) / (len(s1) * 2 - intersect_size)

def similarity_calculations(vectorized_data_words):#, force_recalculate=False):
    start_time = time.time()
    print "Running similarity calculations"
    
    #finding true similarity => vectorized_data_words is composed of bit vectors (numbers)
    #finding signature similarity => vectorized_data_words is composed of lists of numbers (signature)
    currently_calculating_signature_similarity = isinstance(vectorized_data_words[0],list)
    
    similarity = list()
    run_time_complexity =  (len(vectorized_data_words) * (len(vectorized_data_words)+1) )  / 2 
    display_progress_update_iteration = run_time_complexity / 700
    iteration = 0
    
    #compare each file to every other file
    for i in range(0,len(vectorized_data_words)):        
        next_row = list()
        
        for j in range (i,len(vectorized_data_words)):
            jac_sim = 0
            if currently_calculating_signature_similarity:
                jac_sim = jaccard_similarity_of_signatures( vectorized_data_words[i] , vectorized_data_words[j] )
            else:
                jac_sim = jaccard_similarity_of_bit_vectors( vectorized_data_words[i] , vectorized_data_words[j] )
            next_row.append(jac_sim)
            
            iteration += 1
            if( iteration % display_progress_update_iteration == 0 ):#Try to limit display progress changes as writing to output is slow
                progress_float = (iteration + 0.0) / run_time_complexity
                update_progress( progress_float )
        
        similarity.append(next_row)
    
    print ""
    print "Similarity calculation took  "+str(time.time()  - start_time)+" seconds"
    
    return similarity

def next_biggest_prime(x):  
    for i in range(0,len(primes_under_1k)):
        if primes_under_1k[i] > x:
            return primes_under_1k[i]
    
    raise ValueError('Prime could not be found')

#no longer TF-IDF values, just whether or not the word is in the hash. Then translated to a bit vector (number)
# EX) doc = {0, 1.77, .02, 0} TF-IDF values --> doc {0,1,1,0} (word 2 and 3 are present in that doc) --> doc = 0110 = 6
def bit_vectors_of_documents():
    """
    #Use lab2 to get vectors (all ~21k samples)
    tfidf_larger,tfidf_smaller = lab2.get_feature_vectors()
    all_words = lab2.get_unique_words_in_tfidf_data(tfidf_smaller)
    all_class_labels = lab2.get_unique_class_labels_in_tfidf_data(tfidf_smaller) 
    word_vectors, vectorized_class_labels = lab2.get_training_samples_and_class_labels_vectors(tfidf_smaller, all_words, all_class_labels)
    """
    #Use lab4 to get vectors (5k samples)
    word_vectors,class_labels = lab4.get_sample_data(False,False)
    
    for i in range(0,len(word_vectors)):        
        #convert tfidf values to booleans
        for j in range(0,len(word_vectors[i])):
            if word_vectors[i][j] > 0:
                word_vectors[i][j] = 1
        
        #convert boolean list to bit vector (number)
        word_vectors[i] = int( "".join(map(str, word_vectors[i])) , base = 2) #join boolean list into string and parse string to base 2 number
    
    return word_vectors

def hash_efficiency_and_efficacy(vectorized_data_words, true_similarity, num_hashes):
    print ""
    print "Finding efficiency and efficacy of "+str(num_hashes)+" valued document hash signatures" 
    start_time = time.time()
    
    all_doc_signatures = create_hash_signatures(vectorized_data_words, num_hashes)
    siginature_estimated_similarity = similarity_calculations(all_doc_signatures)
    estimate_error = hash_similarity_MSE(true_similarity,siginature_estimated_similarity)
    
    print "Total Mean Squared Error: "+ str(estimate_error)
    print ""

def main():
    print ""
    start_time = time.time()
    vectorized_data_words  = bit_vectors_of_documents()
    
    print ""
    print "Finding true Jaccard similarity between every document..."
    true_similarity = similarity_calculations(vectorized_data_words)
    
    hash_efficiency_and_efficacy(vectorized_data_words,true_similarity,16)
    hash_efficiency_and_efficacy(vectorized_data_words,true_similarity,32)
    hash_efficiency_and_efficacy(vectorized_data_words,true_similarity,64)
    hash_efficiency_and_efficacy(vectorized_data_words,true_similarity,128)
    hash_efficiency_and_efficacy(vectorized_data_words,true_similarity,256)       
    
    
    print "Total running time: "+str(time.time()  - start_time)+" seconds"
    print ""

#calls the main() function
if __name__ == "__main__":
    main()