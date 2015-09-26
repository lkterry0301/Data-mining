import numpy as np
import json
import sys
import os
import imp
from sklearn.neighbors import NearestNeighbors

lab1_dir = os.getcwd()+"/../lab1"
tfidf_dat_path = os.getcwd()+"/../feature_vectors/words_reduced_down_by_tfidf.dat"
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

def get_feature_vectors():
    feature_vectors = list()
    
    if os.path.exists(tfidf_dat_path) and os.path.exists(data_matrix_dat_path):
        tfidf_file = open(tfidf_dat_path, "r")
        data_matrix_file = open(data_matrix_dat_path, "r")

        feature_vectors.append( json.loads( tfidf_file.read() ) )
        feature_vectors.append( json.loads( data_matrix_file.read() ) )

        tfidf_file.close()
        data_matrix_file.close()
    
        print("No need to re-parse original Reuters data, read parsed word data from previous lab1 run. ")
    else:
        feature_vectors = run_lab1_feature_vector_extraction()
    
    return feature_vectors

def run_lab1_feature_vector_extraction():
    print("No .dat files found. Must run lab1 to parse data.")
    lab1 = imp.load_source('lab1_script', lab1_dir+"/lab1_script.py")
    return lab1.get_feature_vectors(original_data_files_directory)

def main():
    feature_vectors = get_feature_vectors()
    tfidf = feature_vectors[0]
    data_matrix = feature_vectors[1]
    
    words_in_tfidf = set()
    
    for row in tfidf:
        for key in row[1].keys():
            words_in_tfidf.add( key )
    
    print "Num words in TFIDF data = "+str(len(words_in_tfidf))
    print "Num words in data matrix = "+str(len(data_matrix[0]))

#calls the main() function
if __name__ == "__main__":
    main()