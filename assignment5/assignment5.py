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

def doc_signature(doc,hash_functions_coefficients):
    p = next_biggest_prime(doc)
    hash_val = ( a * doc + b ) % p
    

def create_hash_functions(num_functions):
    hash_functions_coefficients = list()
    
    for i in range(0,num_functions):
        hash_functions_coefficients.append([random.randrange(1,),random.randrange()])
    
    return hash_functions_coefficients

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
    """
    #check to see if baseline has already been calculated in a previous run. Load and return it if it has
    if os.path.exists(true_similarity_file) and not force_recalculate: 
        print "Using True Similarity calculations from a previous run of this lab. Loading JSON..."
        sim_file = open(true_similarity_file, "r")
        return json.loads( sim_file.read() )
    """
    
    print "Finding True similarity between every document pair. "+str(len(vectorized_data_words))+" documents used. Started at: "+ str(time.ctime(int(time.time())))
    
    true_similarity = list()
    run_time_complexity = len(vectorized_data_words) * len(vectorized_data_words) + 0.0 #(len(vectorized_data_words) * (len(vectorized_data_words)+1))  / (2+0.0)
    display_progress_update_iteration = len(vectorized_data_words) / 1000
    
    #compare each file to every other file
    for i in range(0,len(vectorized_data_words)):
        next_row = list()
        
        for j in range (0,len(vectorized_data_words)):
            v1 = vectorized_data_words[i]
            v2 = vectorized_data_words[j]
            next_row.append(jaccard_similarity_of_bit_vectors(v1,v2)) 
        
        #Try to limit display progress changes as writing to output is slow
        if( i % display_progress_update_iteration == 0 or i == (len(vectorized_data_words)-1) ):
            progress_in_percent = ( (i+1) * len(vectorized_data_words) ) / run_time_complexity
            update_progress( progress_in_percent ) 
        
        true_similarity.append(next_row)
        
    """
    print "Writting baseline similarity to file"
    if os.path.exists(true_similarity_file):
        os.remove(true_similarity_file)
    sim_file = open(true_similarity_file,'w')
    json.dump(true_similarity, sim_file)
    """
    
    return true_similarity

"""
def check_primality(x):
    could_be_prime = fast_might_be_prime_check(x)
    if could_be_prime =="maybe" :
        return miller_rabin(x)
    elif could_be_prime == "isPrime":
        return True
    
    return False

#Miller-Rabin primality test. iteration signifies the accuracy of the test
#at this point, the passed in number is guaranteed to be an odd number not divisible by all the primes under 1k.
#source: https://gist.github.com/bnlucas/5857478
def miller_rabin(n, k=20):
	if n == 2:
		return True
	if not n & 1:
		return False

	def check(a, s, d, n):
		x = pow(a, d, n)
		if x == 1:
			return True
		for i in xrange(s - 1):
			if x == n - 1:
				return True
			x = pow(x, 2, n)
		return x == n - 1

	s = 0
	d = n - 1

	while d % 2 == 0:
		d >>= 1
		s += 1

	for i in xrange(k):
		a = random.randrange(2, n - 1)
		if not check(a, s, d, n):
			return False
	return True

#Check if a number MIGHT be prime by seeing if it is divisble by the small primes first
def fast_might_be_prime_check(x):
    for prime in primes_under_1k:
        if x != prime and x % prime == 0:
            return "no"
        elif x == prime:
            return "isPrime"
    
    return "maybe"

#Bertrand's theorem: for every n > 1 there is always at least one prime p such that n < p < 2n.
def next_biggest_prime(x):    
    if x%2 ==0:
        x+=1
        if check_primality(x):
            return x
    
    while(True):
        x += 2
        if check_primality(x):
            return x
"""
def next_biggest_prime(x):  
    for i in range(0,len(primes_under_1k)):
        if primes_under_1k[i] > x:
            return primes_under_1k[i]
    
    raise ValueError('Prime could not be found')

def bit_vector_from_word_vector(word_v):
    word_v_as_str = "".join(map(str, word_v))
    return int(word_v_as_str,base = 2)

#no longer TF-IDF values, just whether or not the word is in the hash
def vectorized_feature_vectors_indicating_word_presence():
    #Use lab2 to get vectors (all ~21k samples)
    tfidf_larger,tfidf_smaller = lab2.get_feature_vectors()
    all_words = lab2.get_unique_words_in_tfidf_data(tfidf_smaller)
    all_class_labels = lab2.get_unique_class_labels_in_tfidf_data(tfidf_smaller) 
    word_vectors, vectorized_class_labels = lab2.get_training_samples_and_class_labels_vectors(tfidf_smaller, all_words, all_class_labels)
    
    #Use lab4 to get vectors (5k samples)
    #word_vectors,class_labels = lab4.get_sample_data(False,False)
    
    for i in range(0,len(word_vectors)):        
        #convert tfidf values to booleans
        for j in range(0,len(word_vectors[i])):
            if word_vectors[i][j] > 0:
                word_vectors[i][j] = 1
        
        #convert booleans to bit vector
        word_vectors[i] = bit_vector_from_word_vector(word_vectors[i])
    
    return word_vectors

def main():
    print ""
    start_time = time.time()
    
    vectorized_data_words  = vectorized_feature_vectors_indicating_word_presence()
    
    baseline_similarity(vectorized_data_words,True)
    
    print "Total running time: "+str(time.time()  - start_time)+" seconds"
    print ""

#calls the main() function
if __name__ == "__main__":
    main()