import numpy as np
import json
import sys
import os
import imp
from sklearn.neighbors import NearestNeighbors

lab1_dir = os.getcwd()+"/../lab1/"
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
    
    #look to see if dat files exist and we can read in the data, instead of having to run parse words
    for filename in os.listdir(lab1_dir):
        if filename.endswith('.dat'): #parse that data file
            current_data_file = open(lab1_dir+"/"+filename, "r")
            feature_vectors.append( json.loads( current_data_file.read() ) )
            current_data_file.close()
            
            print("No need to re-parse original Reuters data, read preconstructed word data from lab1. Filename: "+filename+" ")
    
    #no dat files were found, thus need to parse the data using lab1
    if( len(feature_vectors) == 0):
        feature_vectors = run_lab1_feature_vector_extraction()
    
    return feature_vectors

#assumes there is only 1 python file in the lab1 directory
def run_lab1_feature_vector_extraction():
    lab1_filename = ''
    
    for filename in os.listdir(lab1_dir):
        if filename.endswith('.py'): #parse that data file
            lab1_filename = filename
    
    lab1 = imp.load_source('lab1_script', lab1_dir+"/"+lab1_filename)
    return lab1.get_feature_vectors(original_data_files_directory)

def main():
    feature_vectors = get_feature_vectors()

#calls the main() function
if __name__ == "__main__":
    main()