# CSE-5243 -- Intro To Data Mining

####Lab 1 Description

To run this program navigate to the lab1 directory and run 
```
python lab1.py #This takes about 4.5 minutes (depending on hardware)
```
The output to the console is 

1. Current status of the program as it runs
2. The length of time the program took to run.
3. A data matrix where the first row is a set of all unique, interesting words in the corpus. Every subsequent row is a list of size two representing a reuters document from the corpus. The first element is a hash map/dictionary representing the class label. Each class label has the elements: topics (set), places (set), and title (string) of a document. The second element is a hash map/dictionary of document's words and number of times that word appears in that document.
4. A list where the first element is class_label and the second is a hash of top [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) valued words for each document in the corpus.
5. A smaller, word reduced version of the above data structure.

The two feature vectors are saved to .dat files as json objects.

####Lab 2 Description

To run this program navigate to the lab2 directory and run 
```
python lab2.py #This takes about 11 minutes to fully complete (depending on hardware)
```
The output to the console is 

1. Data extraction method. If feature vectors from a previous lab1 trial are missing, lab1 will automatically be run again (adds about 5 minutes). Otherwise the data will be parsed almost immediately from the files.
2. A series of 4 cross validation trials. KNN and Decision Tree classifiers are created from a set of words found in Lab1. These words are associated with TF-IDF values and document class labels. The first 2 Cross Validation trials create a KNN and a Decision Tree classifier for a smaller subset of data. The second 2 use a larger set of data and take longer to run.

####Lab 4 Description

To run this program navigate to the assignment4 directory and run 
```
python assignment4.py #This takes about 2.5 minutes to complete. A few seconds for clustering and 2 minutes for quality calculations
```
To run different clustering algorithms, change the code inside the main() function to comment/uncomment different estimator setup lines.

The output to the console is 

1. Time it takes for data processing and clustering to take place
2. Clustering quality: Number of clusters created, Information Gain of clusters, average cluster radius (from centroid), average cluster Sum of Squared Error, and standard deviation of all cluster sizes (number of data points).
3. Total run time

####Resources

* [Class Website](http://web.cse.ohio-state.edu/~srini/674/)
* [Lab 1](http://web.cse.ohio-state.edu/~srini/674/assignment1.doc)
* [Lab 2](http://web.cse.ohio-state.edu/~srini/674/assign2.doc)
