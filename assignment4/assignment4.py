import numpy as np
import time
import json
import sys
import imp
import os
import random
import math
import json
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
lab2 = imp.load_source('lab2', os.getcwd()+"/../lab2/lab2.py")
sampled_data_path = os.getcwd()+"/../feature_vectors/representative_sampled_data_trial.dat"

def std_dev(items):
    mean = sum(items) / len(items)
    
    squared_sum = 0
    for item in items:
        squared_sum += pow(item-mean,2)
    
    return math.sqrt( squared_sum/len(items) )

#magnitude of each vector is 1
def L2_normalization(vectorized_word_arr):
    
    magnitude = 0
    for tfidf_score in vectorized_word_arr:
        magnitude += tfidf_score * tfidf_score
    magnitude = math.sqrt(magnitude)
    
    #if vector is not a zero vector (all positions are zero), normalize all the positions
    if(magnitude != 0):
        for i in range(0,len(vectorized_word_arr)):
            vectorized_word_arr[i] /= magnitude
    #else:
        #How do zero vectors effect approximate spherical K-Means clustering if the vector is not on the unit circle?
    
    return magnitude

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

#centroid is avg feature values of every data point
def cluster_centroid(cluster_data):
    centroid = [0]*len(cluster_data[0])
    #sum up the data values
    for pt in cluster_data:
        for j in range (0, len(centroid) ):
            centroid[j] += pt[j]
    
    #average the centroid
    for i in range(0,len(centroid)):
        centroid[i] = centroid[i] / len(cluster_data)
    
    return centroid

def cluster_centroids(data_partitioned_into_clusters):
    num_clusters = len(data_partitioned_into_clusters)
    centroids = list()
    
    for cluster in data_partitioned_into_clusters:
        centroids.append(cluster_centroid(cluster))
    
    return centroids

def squared_euclidean_dist(pt1,pt2):
    euclidean_dist = 0
    for i in range(0,len(pt1)): #len(pt1) == len(pt2)
        euclidean_dist += pow(pt1[i] - pt2[i],2)
    return euclidean_dist

#SSE = sum squared error
def cluster_radius_and_SSE(cluster_data, centroid):
    radius = 0
    sse = 0
    
    for pt in cluster_data:
        #find distance of pt from centroid
        for i in range(0,len(pt)):
            sqrd_euc_dist = squared_euclidean_dist(pt, centroid)
            radius += math.sqrt(sqrd_euc_dist)/2
            sse += sqrd_euc_dist
    
    radius /= len(cluster_data)
    
    return radius, sse

def clustering_radiuses_and_SSEs(data_partitioned_into_clusters,centroids):
    num_clusters = len(data_partitioned_into_clusters)
    cluster_SSEs = list()
    cluster_radiuses_vals = list()
    
    for i in range(0,num_clusters):
        radius, sse = cluster_radius_and_SSE(data_partitioned_into_clusters[i],centroids[i])
        
        cluster_radiuses_vals.append(radius)
        cluster_SSEs.append(sse)
    
    return cluster_radiuses_vals, cluster_SSEs
"""
#not enough time to implement this
def   silhouette_coefficient(predictions,data,num_clusters):
    
    return
"""
def num_predicitions_in_each_cluster(clustered_data):
    cluster_counts = list()
    for cluster in clustered_data:
        cluster_counts.append( len(cluster) )
    return cluster_counts

def cluster_entropy(class_cluster_counts):    
    entropy = 0
    total_count = sum(class_cluster_counts.values())
    
    for class_index in class_cluster_counts:
        probability_class_in_cluster = (class_cluster_counts[class_index] +0.0) / total_count
        
        entropy_of_class_in_cluster = probability_class_in_cluster * math.log(probability_class_in_cluster,2)
        entropy += entropy_of_class_in_cluster        
    
    return -1 * entropy

def clustering_entropies(classes_in_each_cluster):
    num_clusters = len(classes_in_each_cluster)
    #calculate and return entropies of clusters
    cluster_entropy_values = list()
    for i in range(0,num_clusters):
        cluster_entropy_values.append( cluster_entropy(classes_in_each_cluster[i]) )
    
    return cluster_entropy_values

def information_gain(entropies, data_partitioned_into_clusters,overall_class_counts):
    num_clusters = len(entropies)
    
    parent_entropy = cluster_entropy(overall_class_counts)
    children_entropy = 0
    
    num_data_pts_total = 0
    for cluster in data_partitioned_into_clusters:
        num_data_pts_total += len(cluster)
    
    for i in range(0,num_clusters):
        children_entropy += entropies[i] * ( len(data_partitioned_into_clusters[i])/float(num_data_pts_total) ) #weight each cluster entropy
        
    return parent_entropy - children_entropy

#modifies the original data! Paritioned sampling without replacement
def stratified_sample_data(original_data, original_class_labels, num_sampling_partitions, total_desired_num_samples):
    new_data = list()
    new_class_labels = list()
    
    num_original_data_samples_per_partition = len(original_data) / num_sampling_partitions
    
    for curr_partition in range(num_sampling_partitions-1,-1,-1):
        start_original_data_index = num_original_data_samples_per_partition * curr_partition
        end_original_data_index = num_original_data_samples_per_partition * (curr_partition+1)
        
        num_sampled = 0
        while num_sampled < total_desired_num_samples/num_sampling_partitions: #add a set number of samples per parition iteration
            rand_data_pt = random.randrange(start_original_data_index, end_original_data_index)
            
            new_data.append(original_data[rand_data_pt])
            new_class_labels.append(original_class_labels[rand_data_pt])
            
            #without replacement! Delete from original data as you sample
            del original_data[rand_data_pt]
            end_original_data_index += -1
            num_sampled += 1
    
    return new_data,new_class_labels

#predictions is the estimator's guess of cluster index for each index of the data.
#data is raw (or normalized) values that were used in estimator
#labels is the class labels corresponding to each data point
def cluster_quality(predictions, data, labels):
    print "Determining clustering quality..."+os.linesep
    num_clusters = (max(predictions)+1)
    print "Number of clusters: "+str(num_clusters)
    
    #partition data + classes for ease of use
    data_partitioned_into_clusters = data_in_clusters(num_clusters,predictions, data)
    classes_partitioned_into_clusters, total_class_counts = classes_in_clusters(num_clusters,predictions, labels)
    
    #calculate quality info metrics
    entropies = clustering_entropies(classes_partitioned_into_clusters)    
    cluster_sizes = num_predicitions_in_each_cluster(data_partitioned_into_clusters)
    centroids = cluster_centroids(data_partitioned_into_clusters)
    cluster_radiuses,cluster_SSEs = clustering_radiuses_and_SSEs(data_partitioned_into_clusters, centroids)
    
    #display metrics
    print "Information Gain: "+str(information_gain(entropies,data_partitioned_into_clusters,total_class_counts))
    print "Average Cluster Radius: "+ str( sum(cluster_radiuses)/len(cluster_radiuses) )
    print "Average Cluster SSE: "+ str( sum(cluster_SSEs)/len(cluster_SSEs) )
    print "Standard Deviation in size of clusters: "+str(std_dev(cluster_sizes))
    """
    for i in range(0,num_clusters):
        print "Cluster "+str(i)
        print cluster_info_str(cluster_sizes[i],entropies[i], centroids[i],cluster_radiuses[i],cluster_SSEs[i])
    """
    

def cluster_info_str(size,entropy,centroid,avg_radius,sum_squared_error):
    info_str = ""
    info_str += "Cluster Size: "+str(size)+os.linesep
    info_str += "Cluster entropy: "+str(entropy)+os.linesep
    #info_str += "Cluster Centroid: "+str(centroid)+os.linesep
    info_str += "Cluster radius (average using centroid): "+str(avg_radius)+os.linesep
    info_str += "Cluster Sum of Squared Error (using centroid): "+str(sum_squared_error)+os.linesep
    return info_str

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

def num_unique_classes(doc_class_labels):
    labels = set()
    for doc in doc_class_labels:
        for label in doc:
            labels.add(label)
    return len(labels)


def get_sample_data(l2_normalize,redraw_sampled_data = False):
    print "Getting representative sampled data..."
    vectorized_data_words = None
    vectorized_class_labels = None
    
    if(redraw_sampled_data or not os.path.exists(sampled_data_path) ):
        if os.path.exists(sampled_data_path):
            os.remove(sampled_data_path)
        
        #get the feature vectors
        tfidf_larger,tfidf_smaller = lab2.get_feature_vectors()
        #transform data to be usable with clustering algorithm
        vectorized_data_words, vectorized_class_labels = vectorize_tfidf(tfidf_smaller)
        vectorized_data_words, vectorized_class_labels = stratified_sample_data(vectorized_data_words, vectorized_class_labels, 
                                                                               num_sampling_partitions=20,
                                                                               total_desired_num_samples=5000)
        
        output_sample_data_file = open(sampled_data_path,'w')
        json.dump( [vectorized_data_words, vectorized_class_labels] ,output_sample_data_file)
    else:
        sample_data_file = open(sampled_data_path, "r")
        tmp = json.loads( sample_data_file.read() )
        vectorized_data_words = tmp[0]
        vectorized_class_labels = tmp[1]
    
    if(l2_normalize):
        for pt in vectorized_data_words:
            L2_normalization(pt)
    
    print "Representative sampling yields a dataset with "+str(len(vectorized_data_words) )+" entries."
    
    return vectorized_data_words, vectorized_class_labels

def main():
    print ""
    start_time = time.time()
    
    vectorized_data_words, vectorized_class_labels = get_sample_data(False)
    
    data_proc_time = time.time()  - start_time
    print "Data processing took "+str(data_proc_time)+" seconds"
    
    print "Clustering data..."
    #estimator = KMeans(n_clusters = int(num_unique_classes(vectorized_class_labels)) )
    #estimator = DBSCAN(min_samples=1)
    estimator = DBSCAN(eps=0.53,min_samples=2,metric="cosine",algorithm='brute')
    prediction = estimator.fit_predict(vectorized_data_words)
    
    print "Clustering took "+str(time.time()  - start_time - data_proc_time)+" seconds"
    cluster_quality(prediction, vectorized_data_words, vectorized_class_labels)
        
    print "Total running time: "+str(time.time()  - start_time)+" seconds"
    print ""

#calls the main() function
if __name__ == "__main__":
    main()