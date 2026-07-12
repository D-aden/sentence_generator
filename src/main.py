"""
Markov Chain Text Generator 
    Reads news articles, creates an n-gram Markov model and generates new text
"""

import pandas as pd 
import re 
import random

# READ FILE 

def read_articles(paths):
    """
    Read one or more CSV files and combines the content in their 'article/content/text/body' column into one long string. 
    Parameters: 
        list of one of more file paths
    Returns: 
        one large string made up of all the articles concatenated together 
    """
    if isinstance(paths, str):
        paths = [paths]

    entire_text = []

    for path in paths: 
        # file read using UTF-8 encoding, if that fails, read with cp1252 
        try: 
            df = pd.read_csv(path, encoding='utf-8', sep=None, engine='python', on_bad_lines='skip') 
        except UnicodeDecodeError: 
            df = pd.read_csv(path, encoding='cp1252', sep=None, engine='python', on_bad_lines='skip')
    
        possible_names = ['article', 'content', 'text', 'body']

        # determine if the dataset has one of the approved columns names 
        correct_col = None
        for i in df.columns:
            if i.lower() in possible_names:
                correct_col = i 
                break 
        # raise ValueError if no column is found
        if correct_col is None: 
            raise ValueError(f'No content column found in {path}')

        # remove missing values and convert to string  
        entire_text.extend(df[correct_col].dropna().astype(str))

    # combine all articles into one long string 
    return ' '.join(entire_text)


# CLEAN TEXT

def clean_articles(text):
    """
    Cleans and tokenises article text to be used to build the Markov model. 
    Parameters: 
        a string of combined articles. 
    Returns: 
        a list of lists where each list is a tokenised sentence. 
    """
    # text is lowercased 
    text = text.lower()
    # HTML tags are removed
    text = re.sub(r'<[^>]+>', ' ', text) 
    # URLs are removed, but the puntuation at the end is kept 
    text = re.sub(r'http\S+?(?=[.!?]*(?:\s|$))', ' ', text)

    # text is split into sentences based on the following punctuation '.!?'
    sentences = re.split(r'[.!?]+', text)

    tokens = []

    for sentence in sentences:
        # any characters that aren't letters, digit, whitespace or apostrophes are removed 
        sentence = re.sub(r"[^a-z0-9\s'’]", ' ', sentence)
        # multiple whitespaces are made into one 
        sentence = re.sub(r'\s+', ' ', sentence) 
        # leading and trailing whitespace is removed 
        sentence = sentence.strip()
        # non-empty sentences are split into tokens 
        if sentence:
            tokens.append(sentence.split())

    return tokens

# CREATE NODE AND TRIE CLASS

class Node: 
    """
    Serves as a single node in the trie tree structure.
    Attributes: 
        children: dictionary that links each word of a sequence to its successors
        count: integer that shows how many times a node was at the end of a sequence
    """
    def __init__(self):
        self.children = {}
        self.count = 0

class TrieTree: 
    """
    A trie tree structure that stores word sequences and is used 
    to find successors of a given sequence. 
    """
    def __init__(self):
        # empty trie tree with a single root node created
        self.root = Node()
    
    def add_sequence(self, sequence): 
        """
        Adds sequence to the trie, one word at a time. 
        Parameters: 
            a sequence of words in the form of a list of strings 
        """
        current = self.root 

        for word in sequence:
            if word not in current.children:
                # creates new nodes for unseen words
                current.children[word] = Node()
            current = current.children[word]
        # increments the count at the last node of a sequence (showing that the sequence has been seen)
        current.count += 1
    
    def get_successors(self, sequence):
        """
        Finds possible successors of a given sequence. 
        Parameters: 
            a sequence of words in the form of a list of strings 
        Returns: a tuple made up of two lists: 
            successors: the words found after the given sequence 
            frequencies the number of times a successor has been seen
        If a sequence is not found in the trie, two empty lists are returned.
        """
        current = self.root

        for word in sequence:
            if word not in current.children:
                # sequence not found in trie --> empty lists returned 
                return [], []
            current = current.children[word]
        
        #at the final node, all the successors are placed in a list 
        successors = []
        for word in current.children.keys():
            successors.append(word)
        
        # the corresponding frequencies for each successor are placed in a list 
        freqs = []
        for word in successors:
            freqs.append(current.children[word].count)
        
        return successors, freqs
    
    def __str__(self):
        """
        Illustrates the contents of the trie. 
        Returns: 
            new-line-joined string of up to ten sequences with their corresponding frequencies (i.e 'Hi there (2)')
        """
        sequences = []

        def dfs(node, path):
            # search ends after 10 sequences 
            if len(sequences)>=10:
                return 
            # if an observed sequence is reached (count>0), add to return 
            if node.count > 0: 
                sequences.append((' '.join(path), node.count))
            # continue process with children 
            for word, child in node.children.items():
                dfs(child, path+[word])
        
        dfs(self.root, [])

        return '\n'.join(f'{seq} ({count})' for seq, count in sequences)
        

# CREATE MODEL 

def markov_model(sentences, n=3):
    """
    Builds a Markov model from a list of tokenised sentences. 
    Parameters: 
        tokenised sentences in the form of a list of lists of strings. 
        n: the n-gram order
    Returns: 
        a TrieTree containing every observed sequence and its frequency. 
    """
    model = TrieTree()

    for sentence in sentences:
        # skip sentences that are too short to form a n-gram
        if len(sentence)<n:
            continue 
        # slide a window of size n across the sentence, and add each n-gram to the trie
        for i in range(len(sentence)-n+1):
            sequence = sentence[i:i+n]
            model.add_sequence(sequence)

    return model


# GENERATE TEXT 

def text_generation(model, sentences, n=3, sentence_length=20, num_sentences=20): 
    """
    Generates new text using the built Markov model. 
    Parameters: 
        model: the Markov model as a TrieTree, 
        sentences: tokenised sentences in the form of a list of lists of strings
        n: the n-gram order used to build the Markov model
        sentence_length: the number of words in the sentence 
        num_sentences: the number of sentences in the text
    Returns: 
        the generated text with sentences separated with fullstops. 
    """
    all_sentences = []
    state_len = n-1

    # only sentences longer than the state length is chosen 
    valid_sentences = [s for s in sentences if len(s) > state_len]

    if not valid_sentences:
            return ''

    for i in range(num_sentences):
        attempts = 0
        generated = None 

        # limit of 100 attempts are given to generate a sentence 
        while attempts < 100: 
            attempts += 1 

            # a sentence is randomly selected from the approved sentences 
            source_sentence = random.choice(valid_sentences)
            # starting index is chosen at random, room left for a state
            start = random.choice(range(len(source_sentence) - state_len))
            # initial state is chosen (words of state_len length)
            current = source_sentence[start:start + state_len]

            # loop continues until sentence reaches desired length 
            while len(current) < sentence_length:
                # the last state_len words are chosen as the current state 
                state = current[-state_len:]
                # the successors of this sequence is found + their frequencies 
                successors, freqs = model.get_successors(state)

                if not successors:
                    break 
                
                # a successor is chosen based on its frequency 
                successor = random.choices(successors, weights=freqs)[0]
                # word is added to the sequnce 
                current.append(successor)

            # the attempt is successful if the desired length is reched 
            if len(current) == sentence_length:
                generated = current 
                break 

        if generated is not None:     
            all_sentences.append(' '.join(generated).capitalize())

    return '. '.join(all_sentences) + '.'



if __name__ == '__main__':
    full_text = read_articles(['../data/Articles.csv', '../data/bbc-news-data.csv','../data/cnn_dailymail.csv'])
    tokens = clean_articles(full_text)
    model = markov_model(tokens, n=2)
    print(text_generation(model, tokens, n=2, sentence_length=15, num_sentences=5))

