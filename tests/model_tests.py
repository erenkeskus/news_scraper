import unittest

from news_scraper.data_access.models import Article

class TestModel(unittest.TestCase): 

    def test_news_article_given_identical_values_returns_true(self): 
        values = {
            'title':'Title',
            'sub_title':'sub_title',
            'text':'I am a text.'
            }

        record = Article(**values)
        new_record = Article(**values)

        self.assertTrue(record == new_record)

    def test__two_news_article_with_title_identical_rest_different_returns_false(self): 
        existing_values = {
            'title':'Title',
            'sub_title':'sub_title',
            'text':'I am a text.'
            }
        new_values = {
            'title':'Title',
            'sub_title':'new sub_title',
            'text':'I am a new text.'
        }

        record = Article(**existing_values)
        new_record = Article(**new_values)

        self.assertFalse(record == new_record)        

    def test_two_news_article_with_subtitle_identical_rest_different_returns_false(self): 
        existing_values = {
            'title':'Title',
            'sub_title':'sub_title',
            'text':'I am a text.'
            }
        new_values = {
            'title':'New Title',
            'sub_title':'sub_title',
            'text':'I am a new text.'
        }

        record = Article(**existing_values)
        new_record = Article(**new_values)

        self.assertFalse(record == new_record)        

    def test_two_new_article_with_different_text_only_returns_false(self): 
        existing_values = {
            'title':'Title',
            'sub_title':'sub_title',
            'text':'I am a text.'
            }
        new_values = {
            'title':'Title',
            'sub_title':'sub_title',
            'text':'I am a new text.'
        }

        record = Article(**existing_values)
        new_record = Article(**new_values)

        self.assertFalse(record == new_record)        

suite = unittest.TestLoader().loadTestsFromTestCase(TestModel)
unittest.TextTestRunner(verbosity=2).run(suite)