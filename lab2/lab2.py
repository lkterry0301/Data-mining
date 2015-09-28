import numpy as np
import time
import json
import sys
import os
import imp
from sklearn import tree
from sklearn.neighbors import NearestNeighbors

lab1 = imp.load_source('lab1_script', os.getcwd()+"/../lab1/lab1_script.py")
tfidf_big_dat_path = os.getcwd()+"/../feature_vectors/words_reduced_down_by_tfidf.dat"
tfidf_small_dat_path = os.getcwd()+"/../feature_vectors/words_reduced_more_stringently_by_tfidf.dat"
data_matrix_dat_path = os.getcwd()+"/../feature_vectors/word_data_matrix.dat"
original_data_files_directory = os.getcwd()+"/../data_files"

"""
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
kdt = KDTree(X, leaf_size=30, metric='euclidean')
kdt.query(X, k=2, return_distance=False)          
array([[0, 1],
       [1, 0],
       [2, 1],
       [3, 4],
       [4, 3],
       [5, 4]]...)
"""

def get_KNN_classifier(tfidf_data):
    print ""

#returns a searchable decision tree and a list of words that was used to create training samples in order for that tree (this will be needed for the test data)
def get_decision_tree(tfidf_data):
    print "Building decision tree"
    start_time = time.time()
    
    training_samples = list()
    class_labels = list()
    unique_words = list( get_unique_words_in_tfidf_data(tfidf_data) )
    for row in tfidf_data:
        #get the tfidf values of each unique word for every document. If word is not found in document then set value to 0.
        row_training_samples = list()
        for word in unique_words:
            row_training_samples.append(row[1].get(word,0))
        #add row data to overall data
        training_samples.append(row_training_samples)
        class_labels.append(row[0]['topics'])
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(training_samples, class_labels)
    
    print("Decision Tree creation ran for %s seconds. " % (time.time() - start_time))
    return [clf,unique_words]

def get_unique_words_in_tfidf_data(tfidf_data):
    words = set()
    for row in tfidf_data:
        for key in row[1]:
            words.add(key)
    return words

def load_feature_vectors_from_files():
    feature_vectors = list()
    tfidf_big_file = open(tfidf_big_dat_path, "r")
    tfidf_small_file = open(tfidf_small_dat_path, "r")
    data_matrix_file = open(data_matrix_dat_path, "r")
    
    feature_vectors.append( json.loads( data_matrix_file.read() ) )
    feature_vectors.append( json.loads( tfidf_big_file.read() ) )
    feature_vectors.append( json.loads( tfidf_small_file.read() ) )
    
    tfidf_big_file.close()
    data_matrix_file.close()
    tfidf_small_file.close()
    
    print("No need to re-parse original Reuters data, read parsed word data from previous lab1 run. ")
    
    lab1.print_num_words_in_feature_vectors(feature_vectors[0],feature_vectors[1],feature_vectors[2])
    return feature_vectors

def get_feature_vectors():
    if os.path.exists(tfidf_big_dat_path) and os.path.exists(tfidf_small_dat_path) and os.path.exists(data_matrix_dat_path):
        return load_feature_vectors_from_files()
    else:
        return run_lab1_feature_vector_extraction()

def run_lab1_feature_vector_extraction():
    print("No .dat files found. Must run lab1 to parse data.")
    return lab1.get_feature_vectors(original_data_files_directory)

def main():
    #get the feature vectors
    feature_vectors = get_feature_vectors()
    data_matrix = feature_vectors[0]
    tfidf_larger = feature_vectors[1]
    tfidf_smaller = feature_vectors[1]
    
    #build classifiers for big tfidf data
    tfidf_big_decision_tree_values = get_decision_tree(tfidf_larger)
    
    #build classifiers for small tfidf data
    tfidf_small_decision_tree_values = get_decision_tree(tfidf_smaller)

#calls the main() function
if __name__ == "__main__":
    main()