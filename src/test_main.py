import unittest
from main import clean_articles 
from main import read_articles
from main import TrieTree
from main import Node
from main import markov_model
from main import text_generation
import pandas as pd
import os 
import re

# TEST READ ARTICLES 

class TestReadArticles(unittest.TestCase): 
    def setUp(self):
        self.f1 = 'testcase1.csv'
        self.f2 = 'testcase2.csv'
        pd.DataFrame({'article': ['Hi guys', 'What is up', None], 'id': [1,2,3]}).to_csv(self.f1, index=False)
        pd.DataFrame({'article': ['Hope you are well', 'I am thanks'], 'id': [4,5]}).to_csv(self.f2, index=False)

    
    def tearDown(self):
        os.remove(self.f1)
        if os.path.exists(self.f2):
            os.remove(self.f2)
    
    def test_read_articles(self):
        result = read_articles([self.f1, self.f2])

        expected = 'Hi guys What is up Hope you are well I am thanks'
        self.assertEqual(result, expected)

    def test_one_file(self):
        result = read_articles(self.f1)
        self.assertIn('Hi guys', result)
        self.assertIn('What is up', result)
    
    def test_two_files(self):
        result = read_articles([self.f1, self.f2])
        self.assertIn('Hi guys', result)
        self.assertIn('Hope you are well', result)

    def test_nan_removal(self): 
        result = read_articles(self.f1)
        self.assertNotIn('nan', result.lower())

    def test_column_names(self): 
        other_names = ['content', 'text', 'body']

        for i in other_names: 
            path = 'test_names.csv'
            try: 
                pd.DataFrame({i: ['Hi there'], 'id': [1]}).to_csv(path, index=False)
                result = read_articles(path)
                self.assertIn('Hi there', result)
            finally:
                if os.path.exists(path):
                    os.remove(path)
    
    def test_returns_string(self):
        result = read_articles(self.f1)
        self.assertIsInstance(result, str)

    def test_invalid_column_names(self): 
        path = 'test_invalid.csv'
        try: 
            pd.DataFrame({'Fake_col': ['Hi there']}).to_csv(path, index=False)
            with self.assertRaises(ValueError):
                read_articles(path)
        finally:
            if os.path.exists(path):
                os.remove(path)


# TEST CLEAN ARTICLES 
class TestCleanArticles(unittest.TestCase):

    def test_lowercase(self):
        text = 'Hello There. Lets See If All The Words Are Lowercase'
        assert clean_articles(text) == [['hello', 'there'], ['lets', 'see', 'if', 'all', 'the', 'words', 'are', 'lowercase']]
    
    def test_remove_html(self): 
        text = """
        <html>
        <body>
        <h1>Breaking News</h1>
        <p>Scientists discover a new species in the rainforest.</p>
        <p>The finding has attracted worldwide attention.</p>
        </body>
        </html>
        """
        
        assert clean_articles(text) == [
        ['breaking', 'news',
        'scientists', 'discover', 'a', 'new',
        'species', 'in', 'the', 'rainforest'],
        ['the', 'finding', 'has', 'attracted',
        'worldwide', 'attention']
        ]

    
    def test_remove_urls(self): 
        text = """
        Read the full report at https://example.com/report.
        More details are available at https://news.org/article.
        Researchers say the results are promising and deserve
        further investigation.
        """
        assert clean_articles(text) ==  [
            ['read', 'the', 'full', 'report', 'at'],
            ['more', 'details', 'are', 'available', 'at'],
            ['researchers', 'say', 'the', 'results', 'are',
            'promising', 'and', 'deserve', 'further',
            'investigation']]
   

    def test_allowed_characters(self): 
        result = clean_articles("""
        Wow!!! How’re you today???
        This article... contains lots of punctuation,
        commas, periods, and exclamation marks!!!
        """
        )

        assert result == [
        ['wow'], ['how’re', 'you', 'today'],
        ['this', 'article'], ['contains', 'lots',
        'of', 'punctuation', 'commas', 'periods',
        'and', 'exclamation', 'marks']
        ]

    def test_numbers_remain(self): 
        result = clean_articles('there are 4 apples')
        assert result == [['there', 'are', '4', 'apples']] 
    
    def test_whitespace_removed(self):
        result = clean_articles('there   are    spaces')
        assert result == [['there', 'are', 'spaces']]
    
    def test_edge_cases(self):
        """check that punctuation and empty strings are handles"""
        assert clean_articles('') == []
        assert clean_articles('!!???...,,') == []

class TestNode(unittest.TestCase):
    def test_zero_at_start(self):
        node = Node()
        self.assertEqual(node.count, 0)

    def test_no_children_at_start(self):
        node = Node()
        self.assertEqual(node.children, {})

    def test_children_is_dict(self):
        node = Node()
        self.assertIsInstance(node.children, dict)


class TestTrieTree(unittest.TestCase):
    def setUp(self):
        self.trie = TrieTree()
    
    def test_sequence_retrieval(self):
        self.trie.add_sequence(['a', 'b', 'c'])
        successors, freqs = self.trie.get_successors(['a', 'b'])
        self.assertIn('c', successors)
        
        """check multiple successors case"""
        self.trie.add_sequence(['a', 'b', 'c'])
        self.trie.add_sequence(['a', 'b', 'd'])
        successors, freqs = self.trie.get_successors(['a', 'b'])
        self.assertIn('c', successors)
        self.assertIn('d', successors)

    def test_no_duplicates(self):
        self.trie.add_sequence(['a', 'b', 'c'])
        self.trie.add_sequence(['a', 'b', 'c'])
        successors, freqs = self.trie.get_successors(['a', 'b'])
        index = successors.index('c')
        self.assertEqual(freqs[index], 2)
    
    def test_branch_end(self):
        """a case with no children should return empty"""
        self.trie.add_sequence(['a', 'b', 'c'])
        successors, freqs = self.trie.get_successors(['a', 'b', 'c'])
        self.assertEqual(successors, [])

    #test __str__ 
    def test_str_duplicates(self):
        self.trie.add_sequence(['a', 'b', 'c'])
        self.trie.add_sequence(['a', 'b', 'c'])

        result= str(self.trie)

        self.assertIn('a b c (2)', result)
    
    def test_str_end_frequencies(self):
        self.trie.add_sequence(['a', 'b', 'c'])
        self.trie.add_sequence(['a', 'b'])

        result= str(self.trie)

        self.assertIn('a b c (1)', result)
        self.assertIn('a b (1)', result)

    def test_str_limit(self):
        for i in range(15):
            self.trie.add_sequence([f'word{i}'])
        result=str(self.trie)
        self.assertEqual(result.count('\n'), 9)

class TestMarkovModel(unittest.TestCase):
    def setUp(self):
        self.tokens = [['the', 'monkey', 'fell', 'off', 'the', 'tree'], ['the', 'monkey', 'cried', 'and', 'the', 'monkey', 'fell', 'asleep']]

    def test_returns_trie(self):
        model = markov_model(self.tokens, n=3)
        self.assertIsInstance(model, TrieTree)

    def test_repetition_counts(self): 
        model = markov_model(self.tokens, n=3)
        successors, freqs = model.get_successors(['the', 'monkey'])
        fell_index = successors.index('fell')
        cried_index = successors.index('cried')
        self.assertGreater(freqs[fell_index], freqs[cried_index])

class TestTextGeneration(unittest.TestCase):
    def setUp(self):
        self.tokens = [['the', 'monkey', 'fell', 'off', 'the', 'tree', 'the', 'monkey', 'cried', 'and', 'the', 'monkey', 'fell', 'asleep']]
        self.model = markov_model(self.tokens, n=4)

    
    def test_return_string(self):
        result = text_generation(self.model, self.tokens, n=4, sentence_length=10, num_sentences=3)
        self.assertIsInstance(result, str)

    
    def test_output_not_empty(self):
        result = text_generation(self.model, self.tokens, n=4, sentence_length=10, num_sentences=3)
        self.assertTrue(len(result)>0)
        
    
    def test_number_of_sentences(self):
        num_sentences = 5
        result = text_generation(self.model, self.tokens, n=4, sentence_length=10, num_sentences=num_sentences)
        lst = re.split(r'\. ', result.strip())
        self.assertEqual(len(lst), num_sentences)
    
    def test_length_of_sentences(self):
        sentence_length = 5
        result = text_generation(self.model, self.tokens, n=4, sentence_length=sentence_length, num_sentences=5)
        sentences = [s for s in re.split(r'\. ', result) if s.strip()]
        for s in sentences: 
            self.assertEqual(len(s.split()), sentence_length)




    
if __name__ == '__main__':
    unittest.main()
