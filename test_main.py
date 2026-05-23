import unittest
from main import clean_articles

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
