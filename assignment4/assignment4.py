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
    squared_sum = math.sqrt(squared_sum)
    
    #if vector is not a zero vector (all positions are zero), normalize all the positions
    if(squared_sum != 0):
        for i in range(0,len(vectorized_word_arr)):
            normalized_vector.append( vectorized_word_arr[i] / squared_sum )
    #else:
        #what do I do? Ignore the zero vector? How does this effect approximate spherical K-Means clustering if the vector is not on the unit circle?
    
    return normalized_vector, squared_sum

def data_in_clusters(num_clusters,predictions,data):
    cluster_data = init_list_of_lists(num_clusters)
    
    for i in range(0,len(data)):
        cluster_data[ predictions[i] ].append( data[i] )
    
    return cluster_data

def classes_in_clusters(num_clusters, predictions, all_labels):
    #find the overall count of each class in the data, and the count of each class in each cluster
    total_class_counts = dict()
    classes_in_each_cluster = init_list_of_dicts(num_clusters)
    for i in range(0,len(predictions)):#Note: len(predictions) == len(all_labels)
        for individual_label_index_value in all_labels[i]:#can have multiple labels, so count each label for every doc
            total_class_counts[individual_label_index_value] = total_class_counts.get(individual_label_index_value,0) + 1
            
            cluster_classes = classes_in_each_cluster[ predictions[i] ]
            cluster_classes[individual_label_index_value] = cluster_classes.get(individual_label_index_value,0) + 1#add data's class label to respective predicted cluster
    
    return classes_in_each_cluster, total_class_counts

def cluster_radiuses(num_clusters,predictions,data):
    cluster_radiuses_vals = [0]*num_clusters
    
    max_dist = 0
    
    for i in range(0,len(data)):
        pt1 = data[i]
        for j in range(0,len(data)):    
            pt2 = data[j]
            euclidean_dist = 0
            for index in range(0,len(pt1)): #len(pt1) == len(pt2)
                euclidean_dist += pow(pt1[index] - pt2[index],2)
            euclidean_dist = math.sqrt(euclidean_dist)
            
            euclidean_dist = euclidean_dist/2 #radius is half the distance
            
            if( euclidean_dist > max_dist ):
                max_dist = euclidean_dist
    
    return cluster_radiuses_vals

def   silhouette_coefficient(predictions,data,num_clusters):
    
    return

def num_predicitions_in_each_cluster(clustered_data):
    cluster_counts = list()
    for cluster in clustered_data:
        cluster_counts.append( len(cluster) )
    return cluster_counts

def cluster_entropy(class_cluster_counts, overall_class_counts):    
    entropy = 0
    for class_index in class_cluster_counts:
        probability_class_in_cluster = (class_cluster_counts[class_index] +0.0) / overall_class_counts[class_index]
        
        entropy_of_class_in_cluster = probability_class_in_cluster * math.log(probability_class_in_cluster,2)
        entropy += entropy_of_class_in_cluster        
    
    return -1 * entropy

def clustering_entropies(classes_in_each_cluster, total_class_counts):
    num_clusters = len(classes_in_each_cluster)
    #calculate and return entropies of clusters
    cluster_entropy_values = list()
    for i in range(0,num_clusters):
        cluster_entropy_values.append( cluster_entropy(classes_in_each_cluster[i], total_class_counts) )
    
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
    
    #partition data + classes for ease of use
    data_partitioned_into_clusters = data_in_clusters(num_clusters,predictions, data)
    classes_partitioned_into_clusters, total_class_counts = classes_in_clusters(num_clusters,predictions, labels)
    
    #calculate quality info metrics
    entropies = clustering_entropies(classes_partitioned_into_clusters, total_class_counts)
    cluster_sizes = num_predicitions_in_each_cluster(data_partitioned_into_clusters)
    
    #display metrics
    print "Number of clusters: "+str(num_clusters)
    print "Size of each cluster: "+str( cluster_sizes )
    print "Cluster entropies: "+str( entropies )

def init_list_of_lists(size):
    #cannot use "return [[]] * size" as they are all references to the same list. Adding element to one adds element to all lists!
    list_of_lists = list()
    for i in range(0,size):
        list_of_lists.append( list() )
    return list_of_lists

def init_list_of_dicts(size):
    #cannot use "return [[]] * size" as they are all references to the same list. Adding element to one adds element to all lists!
    list_of_dicts = list()
    for i in range(0,size):
        list_of_dicts.append( dict() )
    return list_of_dicts

def vectorize_tfidf(tfidf_data):
    all_words = lab2.get_unique_words_in_tfidf_data(tfidf_data)
    all_class_labels = lab2.get_unique_class_labels_in_tfidf_data(tfidf_data)
    
    return lab2.get_training_samples_and_class_labels_vectors(tfidf_data, all_words, all_class_labels)
    
def main():
    print ""
    start_time = time.time()
    #get the feature vectors
    tfidf_larger,tfidf_smaller = lab2.get_feature_vectors()
    
    #transform data to be usable with clustering algorithm
    vectorized_data_words, vectorized_class_labels = vectorize_tfidf(tfidf_smaller)
    vectorized_data_words, vectorized_class_labels = stratified_sample_data(vectorized_data_words, vectorized_class_labels, 
                                                                           num_sampling_partitions=20,
                                                                           total_desired_num_samples=5000,
                                                                           l2_normalize_vectors=False)
    
    estimator = KMeans()
    #estimator = DBSCAN()
    #estimator = DBSCAN(metric="cosine",algorithm='brute')
    prediction = estimator.fit_predict(vectorized_data_words)
    cluster_quality(prediction, vectorized_data_words, vectorized_class_labels)
    
    
    print "Total running time: "+str(time.time()  - start_time)+" seconds"
    print ""

#calls the main() function
if __name__ == "__main__":
    main()