import unittest 
from main import clean_articles 
from main import read_articles
from main import TrieTree
from main import Node
from main import markov_model
from main import text_generation

class TestIntegration(unittest.TestCase):

    TEST_TOKENS = [['the', 'monkey', 'fell', 'off', 'the', 'tree'], 
    ['the', 'monkey', 'cried', 'and', 'the', 'monkey', 'fell', 'asleep']]

    def test_read_to_clean_returns_tokens(self):
        text = read_articles('../data/sample.csv')
        tokens = clean_articles(text)
        self.assertIsInstance(tokens, list)
        self.assertTrue(len(tokens) > 0)
        self.assertTrue(all(isinstance(word, str) for sentence in tokens for word in sentence))

    def test_clean_strips_punctuation_from_csv_sentences(self):
        text = read_articles('../data/sample.csv')
        tokens = clean_articles(text)
        words = [word for sentence in tokens for word in sentence]
        self.assertNotIn('mat.', words)
        self.assertIn('mat', words)

    def test_only_content_column_reaches_tokens(self):
        """
        sample.csv has a 'category' column ('Animals', 'Weather', etc.)
        which should never reach the token list 
        test ensures read_articles only pull from the content column
        """
        text = read_articles('../data/sample.csv')
        tokens = clean_articles(text)
        words = [word for sentence in tokens for word in sentence]
        for category_word in ['animals', 'weather', 'nature', 'people', 'transport', 'food', 'education']:
            self.assertNotIn(category_word, words)

    def test_read_to_markov_returns_trietree(self):
        text = read_articles('../data/sample.csv')
        tokens = clean_articles(text)
        trie = markov_model(tokens, n=3)
        self.assertIsInstance(trie, TrieTree)

    def test_trie_learns_transitions_from_csv(self):
        """
        test to confirm data flows through each stage correctly
        'the cat sat on' and 'the dog chased a' both appear in sample.csv
        in the pipeline sequence read → clean → model, the trie must know
        these transitions
        """
        text = read_articles('../data/sample.csv')
        tokens = clean_articles(text)
        trie = markov_model(tokens, n=3)


        successors, _ = trie.get_successors(['the', 'cat', 'sat'])
        self.assertIn('on', successors)


        successors, _ = trie.get_successors(['the', 'dog', 'chased'])
        self.assertIn('a', successors)

    
    def test_entire_pipeline(self): 
        text = read_articles('../data/sample.csv')
        tokens = clean_articles(text)
        trie = markov_model(tokens, n=3)
        result = text_generation(trie, tokens, n=3, sentence_length=10, num_sentences=2)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_trie_only_contains_cleaned_vocab(self):
        """
        test to confirm cleaning happens before model building
        the trie must only know words that come from the cleaned token list
        """
        text = read_articles('../data/sample.csv')
        tokens = clean_articles(text)
        vocab = set(word for sentence in tokens for word in sentence)
        trie = markov_model(tokens, n=3)


        for word in trie.root.children:
            self.assertIn(word, vocab)
    
    def test_generation_sentence_count(self):
        trie = markov_model(self.TEST_TOKENS, n=3)
        for num in [1, 2, 5]:
            result = text_generation(trie, self.TEST_TOKENS, n=3, sentence_length=5, num_sentences=num)
            parts = result.rstrip('.').split('. ')
            self.assertEqual(len(parts), num)

    def test_generation_output_words_in_vocab(self):
        trie = markov_model(self.TEST_TOKENS, n=3)
        vocab = set(word for sentence in self.TEST_TOKENS for word in sentence)
        result = text_generation(trie, self.TEST_TOKENS, n=3, sentence_length=10, num_sentences=5).lower()
        for word in result.replace('.', '').split():
            self.assertIn(word, vocab)

    def test_pipeline_output_words_from_csv_content(self):
        text = read_articles('../data/sample.csv')
        tokens = clean_articles(text)
        vocab = set(word for sentence in tokens for word in sentence)
        trie = markov_model(tokens, n=3)
        result = text_generation(trie, tokens, n=3, sentence_length=10, num_sentences=5)
        for word in result.replace('.', '').split():
            self.assertIn(word, vocab)

    
    def test_ngrams_present_for_each_degree(self):
        for n in range(1, 6):
            full_text = read_articles(['../data/bbc-news-data.csv'])
            sentences = clean_articles(full_text)
            model = markov_model(sentences, n=n)

            for attempt in range(10):
                text = text_generation(model, sentences, n=n, sentence_length=10, num_sentences=5)

                raw_sentences = text.rstrip('.').split('. ')

                for raw_sentence in raw_sentences:
                    words = raw_sentence.lower().split()
                    for i in range(len(words) - (n + 1) + 1):
                        ngram = words[i:i + n + 1]
                        current = model.root
                        for word in ngram:
                            current = current.children.get(word)
                            if current is None: 
                                break 
                        found = current is not None and current.count>0

                        self.assertTrue(found, f"n-gram {ngram} (order {n}) not found in trie")


if __name__ == '__main__':
    unittest.main()
