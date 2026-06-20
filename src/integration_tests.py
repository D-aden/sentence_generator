import unittest 
import random
from main import clean_articles 
from main import read_articles
from main import TrieTree
from main import Node
from main import markov_model
from main import text_generation

class TestIntegration(unittest.TestCase):

    TEST_TOKENS = [
        'the', 'monkey', 'fell', 'off', 'the', 'tree',
        'the', 'monkey', 'cried', 'and', 'the', 'monkey',
        'fell', 'asleep',
    ]

    def test_read_to_clean_returns_tokens(self):
        """pipeline up to tokenisation returns a non-empty list of strings"""
        text = read_articles('data/sample.csv')
        tokens = clean_articles(text)
        self.assertIsInstance(tokens, list)
        self.assertTrue(len(tokens) > 0)
        self.assertTrue(all(isinstance(t, str) for t in tokens))

    def test_clean_strips_punctuation_from_csv_sentences(self):
        """
        test clean_articles removes punctuation 
        since rows in sample.csv ends with a full stop (.)
        after cleaning 'mat.' must appear as 'mat'
        """
        text = read_articles('data/sample.csv')
        tokens = clean_articles(text)
        self.assertNotIn('mat.', tokens)
        self.assertIn('mat', tokens)

    def test_only_content_column_reaches_tokens(self):
        """
        sample.csv has a 'category' column ('Animals', 'Weather', etc.)
        which should never reach the token list 
        test ensures read_articles only pull from the content column
        """
        text = read_articles('data/sample.csv')
        tokens = clean_articles(text)
        for category_word in ['animals', 'weather', 'nature', 'people', 'transport', 'food', 'education']:
            self.assertNotIn(category_word, tokens)

    def test_read_to_markov_returns_trietree(self):
        """
        verify that pipeline from read_article to markov_model
        return a trietree
        """
        text = read_articles('data/sample.csv')
        tokens = clean_articles(text)
        trie = markov_model(tokens)
        self.assertIsInstance(trie, TrieTree)

    def test_trie_learns_transitions_from_csv(self):
        """
        test to confirm data flows through each stage correctly
        'the cat sat' and 'the dog chased' both appear in sample.csv
        in the pipeline sequence read → clean → model the trie must know
        these transitions
        """
        text = read_articles('data/sample.csv')
        tokens = clean_articles(text)
        trie = markov_model(tokens, n=3)


        succs, _ = trie.get_successors(['the', 'cat'])
        self.assertIn('sat', succs)


        succs, _ = trie.get_successors(['the', 'dog'])
        self.assertIn('chased', succs)

    def test_markov_to_generation(self): 
        """
        test that the pipeline from markov_articles to text_generation returns 
        non-empty string
        """
        tokens = ['the', 'monkey', 'fell', 'off', 'the', 'tree', 'the', 'monkey', 'cried', 'and', 'the', 'monkey', 'fell', 'asleep']
        trie = markov_model(tokens)
        result = text_generation(trie, tokens, n=3, sentence_length=10, num_sentences=2) 
        assert isinstance(result, str)
        assert len(result) > 0 
    
    def test_entire_pipeline(self): 
        """
        test the entire pipeline and verify that a non-empty string is returned 
        """
        text = read_articles('data/sample.csv')
        tokens = clean_articles(text)
        trie = markov_model(tokens)
        result = text_generation(trie, tokens, n=3, sentence_length=10, num_sentences=2)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_trie_only_contains_cleaned_vocab(self):
        """
        test to confirm cleaning happens before model building
        the trie must only know words that come from the cleaned token list
        """
        text = read_articles('data/sample.csv')
        tokens = clean_articles(text)
        vocab = set(tokens)
        trie = markov_model(tokens, n=3)


        for word in trie.root.children:
            self.assertIn(word, vocab)
    


    def test_generation_sentence_count(self):
        """
        test to ensure that num_sentences control how many sentences appear in the output
        """
        trie = markov_model(self.TEST_TOKENS)
        for num in [1, 2, 5]:
            result = text_generation(trie, self.TEST_TOKENS, n=3, sentence_length=20, num_sentences=num)
            parts = result.rstrip('.').split('. ')
            self.assertEqual(len(parts), num)

    def test_generation_output_words_in_vocab(self):
        """
        test to confirm words in generated text are from original token vocab
        expects that the model does not invent new words
        """
        trie = markov_model(self.TEST_TOKENS)
        vocab = set(self.TEST_TOKENS)
        result = text_generation(trie, self.TEST_TOKENS, n=3, sentence_length=10, num_sentences=5)
        for word in result.replace('.', '').split():
            self.assertIn(word, vocab)

    def test_pipeline_output_words_from_csv_content(self):
        """
        test that every word in the final output traces back to the sample CSV content column
        confirms if any stage leaks category labels or leaves punctuation attached to tokens
        """
        text = read_articles('data/sample.csv')
        tokens = clean_articles(text)
        vocab = set(tokens)
        trie = markov_model(tokens, n=3)
        result = text_generation(trie, tokens, n=3, sentence_length=10, num_sentences=5)
        for word in result.replace('.', '').split():
            self.assertIn(word, vocab)

    def test_pipeline_is_reproducible(self):
        """same random seed must produce identical output end-to-end"""
        text = read_articles('data/sample.csv')
        tokens = clean_articles(text)
        trie = markov_model(tokens, n=3)

        random.seed(99)
        result1 = text_generation(trie, tokens, n=3, sentence_length=8, num_sentences=3)
        random.seed(99)
        result2 = text_generation(trie, tokens, n=3, sentence_length=8, num_sentences=3)


        self.assertEqual(result1, result2)

if __name__ == '__main__':
    unittest.main()
