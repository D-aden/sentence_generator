import unittest
from main import clean_articles 
from main import read_articles
import pandas as pd
import os 

# TEST READ ARTICLES 

class TestReadArticles(unittest.TestCase): 
    def setUp(self):
        self.f1 = 'testcase1.csv'
        self.f2 = 'testcase2.csv'
        pd.DataFrame({'Article': ['Hi guys', 'What is up', None]}).to_csv(self.f1, index=False)
        pd.DataFrame({'Article': ['Hope you are well', 'I am thanks']}).to_csv(self.f2, index=False)

    def tearDown(self):
        os.remove(self.f1)
        os.remove(self.f2)

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
            pd.DataFrame({{i}: ['Hi there']}).to_csv(path, index=False)
            result = read_articles(path)
            self.assertIn('Hi there', result)
            os.remove(path)


# TEST CLEAN ARTICLES 
class TestCleanArticles(unittest.TestCase):

    def test_lowercase(self): 
        assert clean_articles('Hello There') == ['hello', 'there']
    
    def test_remove_html(self): 
        assert clean_articles('<p>smile</p>') == ['smile']
    
    def test_remove_urls(self): 
        result = clean_articles('see https://something.com for more')
        assert 'https://something.com' not in result 
        assert result == ['see', 'for', 'more']

    def test_allowed_characters(self): 
        result = clean_articles('hi! how are you?')
        assert result == ['hi', 'how', 'are', 'you']

if __name__ == '__main__':
    unittest.main()
