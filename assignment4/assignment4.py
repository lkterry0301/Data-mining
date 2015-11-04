import numpy as np
import time
import json
import sys
import imp
import os
import random
import math
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
lab2 = imp.load_source('lab2', os.getcwd()+"/../lab2/lab2.py")


#magnitude of each vector is 1
def L2_normalization(vectorized_word_arr):
    normalized_vector = list()
    squared_sum = 0
    for tfidf_score in vectorized_word_arr:
        squared_sum += tfidf_score * tfidf_score
    
    #if vector is not a zero vector (all positions are zero), normalize all the positions
    if(squared_sum != 0):
        for i in range(0,len(vectorized_word_arr)):
            normalized_vector.append( vectorized_word_arr[i] / squared_sum )
    #else:
        #what do I do? Ignore the zero vector? How does this effect approximate spherical K-Means clustering if the vector is not on the unit circle?
    
    return normalized_vector, squared_sum

def cluster_entropy(classes_in_cluster, data_with_class_label_indicies_counts):
    #convert classes list to hash representing the number of times a class_index appears in the cluster's class list
    classes = dict()
    for class_index in classes_in_cluster:
        classes[class_index] = classes.get(class_index,0) + 1
    
    """
    print len(classes_in_cluster)
    print num_data_predicted_to_be_in_cluster
    print ""
    """
    
    entropy = 0
    for class_index in classes:
        probability_class_in_cluster = classes[class_index] / data_with_class_label_indicies_counts[class_index]
        """
        print class_index
        print classes[class_index]
        print probability_class_in_cluster
        print ""
        """
        entropy += probability_class_in_cluster * math.log(probability_class_in_cluster,2)
        """
        print classes[class_index]
        print data_with_class_label_indicies_counts[class_index]
        print ""
        """
    
    return -1 * entropy

def clustering_entropies(classes_in_each_cluster, data_with_class_label_indicies_counts):
    num_clusters = len(classes_in_each_cluster)
    
    cluster_entropy_values = list()
    for i in range(0,num_clusters): #Note: len(classes_in_each_cluster) == len(num_predictions_in_each_cluster)
        cluster_entropy_values.append( cluster_entropy(classes_in_each_cluster[i], data_with_class_label_indicies_counts) )
    
    return cluster_entropy_values

def stratified_sample_data(original_data, original_class_labels, num_sampling_partitions, total_desired_num_samples, l2_normalize_vectors):
    new_data = list()
    new_class_labels = list()
    
    num_original_data_samples_per_partition = len(original_data) / num_sampling_partitions
    
    for curr_partition in range(0,num_sampling_partitions):
        
        start_original_data_index = num_original_data_samples_per_partition * curr_partition
        end_original_data_index = num_original_data_samples_per_partition * (curr_partition+1)
        
        while len(new_data) < (total_desired_num_samples / num_sampling_partitions) * (curr_partition+1): #add a set number of samples per parition iteration
            rand_data_pt = random.randrange(start_original_data_index, end_original_data_index)
            normalized_vector, squared_sum = L2_normalization(original_data[rand_data_pt])
            
            if squared_sum != 0:#do not append 0 vectors as they encode no useful info (and cannot be L2 normalized for approximate spherical K-means using SKLearn's Euclidean K-means)
                #append data (normalized if desired) and class label
                if l2_normalize_vectors:
                    new_data.append(normalized_vector)
                else:
                    new_data.append(original_data[rand_data_pt])
                new_class_labels.append(original_class_labels[rand_data_pt])
    
    return new_data,new_class_labels

#predictions is the estimator's guess of cluster index for each index of the data.
#data is raw (or normalized) values that were used in estimator
#labels is the class labels corresponding to each data point
def cluster_quality(predictions, data, labels):
    num_clusters = (max(predictions)+1)
    
    classes_in_each_cluster = [[]] * num_clusters#this variable will track the class labels that are found in each cluster by appending respective class label indicies to needed cluster index
    num_predictions_in_each_cluster = [0] * num_clusters #can be multiple (or none) classes for each data point, so need extra variable to determine
    
    for i in range(0,len(predictions)):#Note: len(predictions) == len(data) == len(labels)
        predicted_data_cluster = predictions[i]
        classes_in_each_cluster[ predicted_data_cluster ].extend(labels[i]) #add data's class label to respective predicted cluster
        num_predictions_in_each_cluster[ predicted_data_cluster ] += 1
    
    
    print "Number of clusters: "+str(num_clusters)
    print "Size of each cluster: "+str(num_predictions_in_each_cluster)
    print "Cluster entropies: "+str( clustering_entropies(classes_in_each_cluster, class_label_indicies_counts(labels) ) )

def class_label_indicies_counts(all_labels):
    label_counts = dict()
    
    for data_points_class_labels in all_labels:
        for individual_label_index_value in data_points_class_labels:
            label_counts[individual_label_index_value] = label_counts.get(individual_label_index_value,0) + 1
    
    return label_counts

def vectorize_tfidf(tfidf_data):
    all_words = lab2.get_unique_words_in_tfidf_data(tfidf_data)
    all_class_labels = lab2.get_unique_class_labels_in_tfidf_data(tfidf_data)
    
    return lab2.get_training_samples_and_class_labels_vectors(tfidf_data, all_words, all_class_labels)
    
def main():
    start_time = time.time()
    #get the feature vectors
    tfidf_larger,tfidf_smaller = lab2.get_feature_vectors()
    
    #transform data to be usable with clustering algorithm
    vectorized_data_words, vectorized_class_labels = vectorize_tfidf(tfidf_smaller)
    vectorized_data_words, vectorized_class_labels = stratified_sample_data(vectorized_data_words, vectorized_class_labels, 
                                                                           num_sampling_partitions=20,
                                                                           total_desired_num_samples=5000,
                                                                           l2_normalize_vectors=True)
    
    #estimator = KMeans()
    #estimator = DBSCAN()
    estimator = DBSCAN(metric="cosine",algorithm='brute')
    prediction = estimator.fit_predict(vectorized_data_words)
    cluster_quality(prediction, vectorized_data_words, vectorized_class_labels)
    
    
    print "Total running time: "+str(time.time()  - start_time)+" seconds"

#calls the main() function
if __name__ == "__main__":
    main()