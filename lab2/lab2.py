import numpy as np
import json
import sys
import os
import imp
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

from sklearn import tree

"""
X = [[0, 0], [1, 1]]
Y = [0, 1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
"""
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
    feature_vectors = get_feature_vectors()
    data_matrix = feature_vectors[0]
    tfidf_larger = feature_vectors[1]
    tfidf_smaller = feature_vectors[1]
    

#calls the main() function
if __name__ == "__main__":
    main()