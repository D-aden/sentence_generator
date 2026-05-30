"""
Markov Chain Text Generator 
- reads news articles, creates an n-gram Markov model and produces new text
"""

import pandas as pd 
import re 
import random

# READ FILE 

def read_articles(path):
    """returns string made up of all the articles"""
    df = pd.read_csv(path, encoding='cp1252')
    articles = df['Article']
    full_text = ' '.join(articles.dropna().astype(str))
    return full_text


# CLEAN TEXT

def clean_articles(text):
    """
    steps: 
        - converts text to lowercase, removes html tags, removes urls, only allows certain characters, 
          fixes internal whitespace, removes leading and trailing whitespace
    
    returns a list of tokens
    """
    text = text.lower()
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    tokens = text.split()

    return tokens

# CREATE NODE AND TRIE CLASS

class Node: 
    def __init__(self):
        """
        - self.children links each word of a sequence to a possible successor
        - self.count shows how many times a node was at the end of a sequence
        """
        self.children = {}
        self.count = 0

class TrieTree: 
    def __init__(self):
        self.root = Node()
    
    def add_sequence(self, sequence): 
        """
        - adds sequences to the trie, one word at a time 
        - creates new nodes for unseen words
        - increments the count at the last node of a sequence (then means that the sequence has been seen)
        """
        current = self.root 

        for w in sequence:
            if w not in current.children:
                current.children[w] = Node()
            current = current.children[w]
        
        current.count += 1
    
    def get_successors(self, sequence):
        """
        - returns two lists: successors (the words found after the given word) and 
          frequencies (the number of times a successor has been seen)
        """
        current = self.root

        for w in sequence:
            if w not in current.children:
                return [], []
            current = current.children[w]
        
        successors = []
        for w in current.children.keys():
            successors.append(w)
        
        freqs = []
        for w in successors:
            freqs.append(current.children[w].count)
        
        return successors, freqs
    
    def __str__(self):
        return str(self.root.children)
        

# CREATE MODEL 

def markov_model(tokens, n=3):
    """
    - n-grams are extracted from the 'tokens' list (using sliding windows)
      and added to the trie as a sequence.
    
    - a TrieTree containing every observed sequence and its frequency is returned
    """
    t = TrieTree()

    for i in range(len(tokens)-n+1):
        sequence= tokens[i:i+n]
        t.add_sequence(sequence)

    return t


# GENERATE TEXT 

def text_generation(t, tokens, n=3, length=50): 
    """
    - extracts a sequence from the tokens list, 
    - in the loop: 
        - window shifts to the right, successors and frequencies are taken from the TrieTree, 
          weighted random choice is computed 
    - the loop ends if the length is reached or no successors are found 
    - generated string is returned 
    """
    state_len = n-1

    start = random.choice(range(len(tokens) - state_len))
    generated = tokens[start:start + state_len]

    for i in range(length):
        state = generated[-state_len:]
        successors, freqs = t.get_successors(state)

        if not successors:
            break 
        
        successor = random.choices(successors, weights=freqs)[0]
        generated.append(successor)
    

    return ' '.join(generated)



if __name__ == '__main__':
    full_text = read_articles('data/Articles.csv')
    tokens = clean_articles(full_text)
    m = markov_model(tokens, n=3)
    print(text_generation(m, tokens, n=3, length=100))