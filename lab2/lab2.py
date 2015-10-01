import numpy as np
import time
import json
import sys
import os
import imp
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier

lab1 = imp.load_source('lab1_script', os.getcwd()+"/../lab1/lab1_script.py")
tfidf_big_dat_path = os.getcwd()+"/../feature_vectors/words_reduced_down_by_tfidf.dat"
tfidf_small_dat_path = os.getcwd()+"/../feature_vectors/words_reduced_more_stringently_by_tfidf.dat"
data_matrix_dat_path = os.getcwd()+"/../feature_vectors/word_data_matrix.dat"
original_data_files_directory = os.getcwd()+"/../data_files"

def get_KNN_classifier(tfidf_data, unique_words_in_tfidf_data, unique_class_labels):
    print "Building KNN Classifier  ("+str(len(unique_words_in_tfidf_data))+" words)"
    start_time = time.time()
    
    training_samples,class_labels = get_traning_samples_and_class_labels_vectors(tfidf_data, unique_words_in_tfidf_data, unique_class_labels)
    
    neigh = KNeighborsClassifier()
    neigh.fit(training_samples,class_labels)
    
    return neigh, (time.time() - start_time)

#returns a searchable decision tree and a list of words that was used to create training samples in order for that tree (this will be needed for the test data)
def get_decision_tree(tfidf_data, unique_words_in_tfidf_data, unique_class_labels):
    print "Building decision tree ("+str(len(unique_words_in_tfidf_data))+" words)"
    start_time = time.time()
    
    training_samples,class_labels = get_traning_samples_and_class_labels_vectors(tfidf_data, unique_words_in_tfidf_data, unique_class_labels)
    
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(training_samples, class_labels )
    
    return clf, (time.time() - start_time)

def get_traning_samples_and_class_labels_vectors(tfidf_data, unique_words_in_tfidf_data, unique_class_labels):
    training_samples = list()
    class_labels = list()
    
    for document in tfidf_data:
        #transform the class labels to int's using the overall class labels
        doc_class_label = list()
        if len(document[0]['topics']) == 0:#no/empty class label
                doc_class_label.append( unique_class_labels.index('') )            
        else:
            for topic in document[0]['topics']:
                doc_class_label.append( unique_class_labels.index(topic) )
        class_labels.append(doc_class_label)
        
        #convert words in each document to a vector and add to training samples
        doc_training_samples = vectorize_document_words(document[1],unique_words_in_tfidf_data)
        training_samples.append(doc_training_samples)
    
    return training_samples,class_labels

def get_unique_words_in_tfidf_data(tfidf_data):
    words = set()
    for doc in tfidf_data:
        for key in doc[1]:
            words.add(key)
    return list(words)

def vectorize_document_words(word_dict,all_unique_words_across_docs):
    word_vector = list()
    for word in all_unique_words_across_docs:
        word_vector.append(word_dict.get(word,0))
    return word_vector

def get_unique_class_labels_in_tfidf_data(tfidf_data):
    words = set()
    for doc in tfidf_data:
        for topic in doc[0]['topics']:
            words.add(topic)
    return ['']+list(words) #prepend empty class label

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

def pretty_print_prediction(all_class_labels,prediction):
    classes = ''
    index_of_none_class = all_class_labels.index('')
    for class_index in prediction[0]:
        if class_index == index_of_none_class:
            classes = "NONE TOPIC" + ", "+classes  
        else:
            classes = all_class_labels[class_index] +", "+classes                
    print "Topics: "+classes[:-2] #remove comma and space from the end of string

def cross_validation_accuracy(tfidf_data, num_subsets, classifier_type):
    print ""
    print "Running Cross Validation...subsets based on number of documents, not words. Thus number of training words may vary"
    num_samples_in_one_subset = len(tfidf_data) / num_subsets
    total_query_time = 0
    total_classifier_build_time = 0
    total_train_num_words = 0
    num_queries = 0
    num_correct = 0
    num_incorrect = 0
    #rotate through subsets in the data to perform cross validation accuracy calculations
    for current_validation_test in range(0,num_subsets):
        pos = current_validation_test * num_samples_in_one_subset
        
        #use one subset for the test data, and all the other subsets for the train data
        tfidf_test = tfidf_data[pos:(pos + num_samples_in_one_subset)]
        tfidf_train = tfidf_data[:pos] + tfidf_data[(pos + num_samples_in_one_subset):]
        train_unique_words = get_unique_words_in_tfidf_data(tfidf_train)
        train_class_labels = get_unique_class_labels_in_tfidf_data(tfidf_train)
        
        total_train_num_words += len(train_unique_words)
        
        classifier = None
        build_time = 0
        if classifier_type.lower() == 'knn':
            classifier,build_time = get_KNN_classifier(tfidf_train, train_unique_words, train_class_labels)
        elif classifier_type.lower() == 'decision tree':
            classifier,build_time = get_decision_tree(tfidf_train, train_unique_words, train_class_labels)
        else:
            raise ValueError('Invalid classifier name passed to Cross Validation Accuracy checking!')
        total_classifier_build_time += build_time
        
        print "Running cross validation predictions..."
        for doc in tfidf_test:
            #run a prediction on this document using the above model
            query = vectorize_document_words(doc[1],train_unique_words)
            start_time = time.time()
            prediction = classifier.predict(query)
            total_query_time = total_query_time + (time.time() - start_time)
            num_queries = num_queries + 1
            
            #determine this prediction's accuracy and keep track of overall accuracy
            num_doc_correct, num_doc_incorrect = num_correct_and_incorrect_classes(doc[0]['topics'], train_class_labels, prediction)
            num_correct += num_doc_correct
            num_incorrect += num_doc_incorrect
        
        print "Cross validating "+classifier_type.upper()+" accuracy..."+ str(current_validation_test+1) +" out of "+str(num_subsets)+" completed!"
    
    print ""
    print "Cross Validation completed!"
    print "     Average "+classifier_type.upper()+" classifier build time (offline): " + str(total_classifier_build_time / num_subsets)
    print "     Average num words used to train classifier: " + str(total_train_num_words / num_subsets)
    print "     Average classification time (online): " + str(total_query_time / num_queries)
    print "     Total Accuracy (#correct classes / #correct+#incorrect): " + "{0:.5f}%".format( (num_correct / float(num_correct + num_incorrect)) * 100)
    print ""

def num_correct_and_incorrect_classes(correct_topics, all_class_labels, prediction):
    index_of_none_class = all_class_labels.index('')
    
    correct_topics_indicies = list()
    #convert the 'correct topics' to indices of the all_class_labels list to be comparable with prediction
    if len(correct_topics) == 0:
        correct_topics_indicies.append(index_of_none_class)
    else:
        for topic in correct_topics:
            index = all_class_labels.index(topic) if topic in all_class_labels else None
            if index != None:
                correct_topics_indicies.append( index )
    
    #find false and true positives 
    intersection = set(correct_topics_indicies) & set(prediction[0])
    num_correct = len( intersection ) #size of real intersect predicted
    num_incorrect = len(correct_topics_indicies) + len( prediction[0] ) - len(intersection) #Num missed classes + num incorrect classes - num correct classes
    
    return num_correct, num_incorrect

def main():
    start_time = time.time()
    #get the feature vectors
    feature_vectors = get_feature_vectors()
    tfidf_larger = feature_vectors[1]
    tfidf_smaller = feature_vectors[2]
    feature_vectors = None #remove feature_vectors[0], the data matrix, from memory as it is not needed
    
    cross_validation_accuracy(tfidf_smaller,4,'knn')
    cross_validation_accuracy(tfidf_smaller,4,'decision tree')
    
    cross_validation_accuracy(tfidf_larger,4,'knn')
    cross_validation_accuracy(tfidf_larger,4,'decision tree')
    
    print "Total running time: "+str(time.time()  - start_time)+" seconds"

#calls the main() function
if __name__ == "__main__":
    main()