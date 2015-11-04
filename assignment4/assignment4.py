import numpy as np
import time
import json
import sys
import imp
import os
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
lab2 = imp.load_source('lab2', os.getcwd()+"/../lab2/lab2.py")
"""
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
"""

"""
from sklearn.metrics.pairwise import cosine_similarity
def new_euclidean_distances(X, Y=None, Y_norm_squared=None, squared=False):
    return cosine_similarity(X,Y)

# monkey patch (ensure cosine dist function is used)
from sklearn.cluster import k_means_k_means_.euclidean_distances 

k_means_.euclidean_distances = new_euclidean_distances 
"""

def min_max_normalization(vectorized_word_arr):
    min_val = sys.maxint
    max_val = - sys.maxint
    
    for doc in vectorized_word_arr:
        for tfidf_score in doc:
            if(tfidf_score > max_val):
                max_val = tfidf_score
            if(tfidf_score < min_val):
                min_val = tfidf_score
    
    diff = max_val - min_val
    for doc in vectorized_word_arr:
        for i in range(0,len(doc)):
            doc[i] = (doc[i] - min_val) / diff

def vectorize_tfidf(tfidf_data):
    all_words = lab2.get_unique_words_in_tfidf_data(tfidf_data)
    all_class_labels = lab2.get_unique_class_labels_in_tfidf_data(tfidf_data)
    
    return lab2.get_training_samples_and_class_labels_vectors(tfidf_data, all_words, all_class_labels)
    
def main():
    start_time = time.time()
    #get the feature vectors
    tfidf_larger,tfidf_smaller = lab2.get_feature_vectors()
    
    #transform data to be usable with clustering algorithm
    vectorized_data_words, vectorized_data_labels = vectorize_tfidf(tfidf_smaller)
    min_max_normalization(vectorized_data_words)
    """
    #C = 1 - cosine_similarity(vectorized_data_words)
    #print C
    ward = AgglomerativeClustering(n_clusters=10, linkage='ward').fit(vectorized_data_words)
    """
    
    #estimator = KMeans()
    #estimator = DBSCAN()
    #estimator = DBSCAN(metric="cosine",algorithm='brute')
    #estimator.fit_predict(vectorized_data_words)
    
    
    print "Total running time: "+str(time.time()  - start_time)+" seconds"

#calls the main() function
if __name__ == "__main__":
    main()