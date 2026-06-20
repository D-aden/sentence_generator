# Specification Document

## Sentence Generation Using Markov Chains

- **Study Program:** Bachelor of Science (BSc)
- **Language used in the project documentation:** English
- **Which programming language are you using?** Python
- **Also, mention any other languages you are proficient in to the extent that you could peer-review projects written in them.** Python, Java

#### - What algorithms and data structures qill you implement in your project?
- Text preprocessing (i.e tokenisation, sentence splitting and stopword removal)
- N-gram Markov chain construction (bigram/trigram transition tables)
- Random sentence generation 
- Data structures: lists, dictionaries, tuples, arrays

#### - What problem are you solving?
- The program allows a user to take any text corpus and produce sentences that resemble the input text in style and tone. This will make text generation faster and easier. 


#### - What inputs does the program receive, and how are they used? 
The program accepts one or more text corpora, such as:
- Input: any text corpus (novels, poems, articles etc.)
- The input is processed and the frequency of word pairings are evaluated to predict what word might follow another. The data is then taken and used to yield sentences based on these probabilities.


#### - Expected time and space complexities (e.g Big-O analysis)?
- Preprocessing: O(n) time and space (proportional to the size of input)
- Markov chain construction: O(n) time, O(n+m) space (where n are the states and m are the transitions)
- Random sentence generation: O(n) time and space (‘n’ words and each word is searched once)


#### - List of sources you intend to use:

-  Jurafsky, D., & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed., draft). Available at: https://web.stanford.edu/~jurafsky/slp3/
-  Manning, C. D., & Schütze, H. (1999). *Foundations of Statistical Natural Language Processing*. MIT Press.
