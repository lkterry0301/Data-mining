import numpy as np
import time
import json
import sys
import imp
import os

lab2 = imp.load_source('lab2', os.getcwd()+"/../lab2/lab2.py")

def main():
    start_time = time.time()
    #get the feature vectors
    tfidf_larger,tfidf_smaller = lab2.get_feature_vectors()
    
    
    
    print "Total running time: "+str(time.time()  - start_time)+" seconds"

#calls the main() function
if __name__ == "__main__":
    main()