# CSE-5243 -- Intro To Data Mining

####Lab 1 Description

To run this program navigate to the lab1 directory and run 
```
python lab1.py #This takes about 4.5 minutes, varying depending upon your hardware
```
The output to the console is 

1. Current status of the program as it runs
2. The length of time the program took to run.
3. A list where the first element is class_label and the second is a hash of top [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) valued words. 
4. A data matrix where the first row is a set of all unique, interesting words in the corpus. Every subsequent row is a list of size two representing a reuters document from the corpus. The first element is a hash map/dictionary representing the class label. Each class label has the elements: topics (set), places (set), and title (string) of a document. The second element is a hash map/dictionary of document's words and number of times that word appears in that document.

The two feature vectors are seaved to .dat files as json objects.

####Lab 2 Description

To run this program navigate to the lab2 directory and run 
```
python lab2.py #This takes about --- minutes, varying depending upon your hardware
```
The output to the console is 

1. The length of time the program took to run.
2. 

####Resources

* [Class Website](http://web.cse.ohio-state.edu/~srini/674/)
* [Lab 1](http://web.cse.ohio-state.edu/~srini/674/assignment1.doc)
