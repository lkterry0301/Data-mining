#import numpy as np
import json
import sys
import os
import imp
#from sklearn.neighbors import NearestNeighbors
lab1 = imp.load_source('lab1_script', os.getcwd()+"/../lab1/lab1_script.py")


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

#from sklearn import tree

"""
X = [[0, 0], [1, 1]]
Y = [0, 1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
"""

def main():
    feature_vectors = lab1.get_feature_vectors(os.getcwd()+"/../data_files")
    

#calls the main() function
if __name__ == "__main__":
    main()