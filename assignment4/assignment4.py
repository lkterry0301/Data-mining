import numpy as np
import time
import json
import sys
import imp
import os
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
lab2 = imp.load_source('lab2', os.getcwd()+"/../lab2/lab2.py")

def vectorize_tfidf(tfidf_data):
    document_vectors = list()
    all_words = lab2.get_unique_words_in_tfidf_data(tfidf_data)
        
    for document in tfidf_data:
        document_vectors.append(lab2.vectorize_document_words(document[1],all_words))
    
    return document_vectors
    
def main():
    start_time = time.time()
    #get the feature vectors
    tfidf_larger,tfidf_smaller = lab2.get_feature_vectors()
    
    estimator = KMeans()
    #estimator = DBSCAN()
    small_data = vectorize_tfidf(tfidf_smaller)
    estimator.fit_predict(small_data)
    
    print "Total running time: "+str(time.time()  - start_time)+" seconds"

#calls the main() function
if __name__ == "__main__":
    main()