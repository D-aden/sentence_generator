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



# CREATE MODEL 

def markov_model(tokens, n=3):
    """
    returns a nested dictionary: 
        - keys: states (as strings)
        - values: dictionary with next possible words as keys and probabilities as values.  
    """
    d = {}

    for i in range(len(tokens)-n+1):
        state = tuple(tokens[i:i+n-1])
        nextword = tokens[i+n-1]
        
        if state not in d: 
            d[state] = {}

        if nextword in d[state]:
            d[state][nextword] += 1
        else: 
            d[state][nextword] = 1
    
    for wordcount in d.values():
        total = 0 
        for num in wordcount.values():
            total += num
        
        for word in wordcount: 
            wordcount[word] = wordcount[word]/total 
    
    final_dict = {' '.join(key): val for key ,val in d.items()}
    
    return final_dict



# GENERATE TEXT 


def text_generation(m, n=3, length=50): 
    """
        - starting state (string) is randomly chosen 
        - next word is chosen by weighted random choice and appended to state words
        - starting state is adjusted so that it no longer includes the first word
        - function loops
        - list of state words are converted into a string and returned.
    """
    starting_state = random.choice(list(m))
    state_words = starting_state.split()

    for i in range(length):
        probs = list(m[starting_state].values())
        nextword = random.choices(list(m[starting_state]), weights=probs)[0]
        state_words.append(nextword)
        starting_state = ' '.join(state_words[-(n-1):])
    
    return ' '.join(state_words)

if __name__ == '__main__':
    full_text = read_articles('data/Articles.csv')
    tokens = clean_articles(full_text)
    m = markov_model(tokens, n=3)
    #print(m['to the'])

    print(text_generation(m))