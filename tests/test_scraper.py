import unittest
import os

from news_scraper import app_root
from news_scraper.scraper.scraper import parse_articles, retrieve_page

class TestScraper(unittest.TestCase): 

    @classmethod
    def setUp(cls): 
        cls.file_path = os.path.join(app_root, 'tests', 'International - DER SPIEGEL.html')

    def test_article_title_correct(self):
        with open(TestScraper.file_path, 'r') as f: 
            tested = parse_articles(f)[0]['title']

        asserted = '"A Cold War with China Is Probable and Not Just Possible"'

        self.assertEqual(tested, asserted)

    def test_article_sub_title_correct(self):
        with open(TestScraper.file_path, 'r') as f: 
            tested = parse_articles(f)[0]['sub_title']

        asserted = 'Former Australian Prime Minister Kevin Rudd'

        self.assertEqual(tested, asserted)

    def test_article_text_correct(self):
        with open(TestScraper.file_path, 'r') as f: 
            tested = parse_articles(f)[0]['text']

        asserted = ('China presents a significant threat, believes former Australian Prime Minister Kevin Rudd.'
                    +' Which is why, he says, the West must work together rather than engage in the kind of bickering '
                    +'triggered by the recent submarine deal between Australia and the United States.')

        self.assertEqual(tested, asserted)

    def test_number_of_articles_are_equal_to_four(self): 
        with open(TestScraper.file_path, 'r') as f: 
            tested = len(parse_articles(f))  
    
            asserted = 4
            self.assertEqual(tested, asserted)

    def test_last_article_title_is_correctly_the_last_title(self): 
        with open(TestScraper.file_path, 'r') as f: 
            tested = parse_articles(f)[3]['title']

        asserted = ('The Changing Virus')

        self.assertEqual(tested, asserted)


suite = unittest.TestLoader().loadTestsFromTestCase(TestScraper)
unittest.TextTestRunner(verbosity=2).run(suite)
