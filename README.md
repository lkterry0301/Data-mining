# CSE-5243 -- Intro To Data Mining

####Lab 1 Description
To run this program navigate to the lab1 directory and run 
```
python lab1.py
```
The output to the console is 

1. The length of time the program took to run.
2. A set of 500 words representing the words in the corpus with the highest [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) scores.
3. A data matrix where the first row is a set of all unique, interesting words in the corpus. Every subsequent row is a list of size two representing a reuters document from the corpus. The first element is the class label: a hash map/dictionary with the elements topics (set), places (set), and title (string) of a document. The second element is a hash map/dictionary with keys of interesting words in that document and values of the number of times that word appears in the document.

####Resources

* [Class Website](http://web.cse.ohio-state.edu/~srini/674/)
* [Lab 1](http://web.cse.ohio-state.edu/~srini/674/assignment1.doc)
