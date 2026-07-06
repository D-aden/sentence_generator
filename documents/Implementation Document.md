# Implementation Document 

### The General Structure of the Program
The program begins with ‘read_articles’, which loads one or more CSV files, finds the column containing the article text, and combines all of the articles into a single string. This text is then passed to ‘clean_articles’, where it is converted to lowercase, cleaned of HTML tags and URLs, split into sentences, and stripped of punctuation and unnecessary whitespace. Instead of returning one large list of words, the function returns a list of tokenised sentences.

The ‘Node’ class represents an individual node in the trie structure. Each node stores a children's dictionary containing links to subsequent words and a count value that records how many times a sequence ends at that node. The TrieTree’s ‘add_sequence’ method inserts word sequences and updates the count of the final node, while ‘get_successors’ retrieves all possible next words for a given state along with their frequencies.

The markov_model function constructs the n-gram model using the trie. It moves a sliding window of size n across each tokenised sentence and adds every resulting n-gram to the ‘TrieTree’. The final stage is handled by ‘text_generation’, which generates new sentences of a specified length. It starts by selecting a random state from the model, then repeatedly chooses the next word based on the frequencies stored in the trie. If a sequence cannot be continued before reaching the desired length, the function selects a new starting state and tries again. Once complete, the generated words are joined into sentences, capitalised, and combined to produce the final text.




### Achieved Time Complexity 

| Function                  | Time Complexity |
|---------------------------|-----------------|
| `read_articles`             | O(n), where *n* is the total size of the CSV files |
| `clean_articles`            | O(n), where *n* is the length of the input string |
| `TrieTree.add_sequence()`   | O(n), where *n* is the length of the sequence |
| `TrieTree.get_successors()` | O(k + n), where *k* is the cost of traversing the tree and *n* is the cost of collecting successors |
| `markov_model`              | O(n), where *n* is the total number of tokens |
| `text_generation`           | O(n · l · k), where *n* is the number of sentences, *l* is the sentence length, and *k* is the time complexity of `get_successors()` |



### Possible shortcomings and suggestions for improvements
- More work is required to improve the intelligibility of the generated sentences, for example through the use of part-of-speech tagging.
- The preprocessing performed in ‘clean_articles’ needs to be fine-tuned to ensure that isolated characters and other anomalies do not appear in the generated text.
- Sentence splitting could be performed using patterns such as ‘, but’, ‘, and’, and ‘, so’ in order to avoid forcing highly contrasting ideas into the same sentence.
- Numbers could be normalised so that the model treats ‘3’ and ‘three’ as equivalent. This could be achieved by converting digits into their corresponding word forms.
- Contractions could be normalised so that expressions such as “don't” and “do not” are treated as equivalent. This could be implemented using a dictionary that maps contractions to their expanded forms.
- It could be useful for the model to distinguish between a sentence that has reached a natural ending and one that terminates because the final word has no successors. This distinction would help develop organic text.
 


### Use of large language models 
#### - Claude was used for the following: 
- Debugging implementation issues
- Clarifying Markov chain fundamentals
- Understanding trie data structures
- Creating a sample.csv file for testing 
- Creating text for several unit tests 
- Helping fix markdown formating issues  
- Helping with the aesthetics of the GUI


### List of the sources you have used, only those relevant to your work.
- https://www.geeksforgeeks.org/nlp/markov-chains-in-nlp/
- https://en.wikipedia.org/wiki/Markov_chain
- https://www.geeksforgeeks.org/dsa/trie-insert-and-search/
- https://en.wikipedia.org/wiki/Trie

