import unittest
import datetime

from news_scraper.data_access.data_access import init_db
from news_scraper.data_access.data_access import add_new_record
from news_scraper.data_access.data_access import session_scope
from news_scraper.data_access.models import Article, ArticleOccurenceLog


db_uri = 'sqlite:///:memory:'
class TestDataAccess(unittest.TestCase): 

    @classmethod
    def setUp(cls):
        cls.engine = init_db(db_uri)
        with session_scope(engine=cls.engine) as session: 
            tested = session.query(Article).all()

    def test_new_article_gets_inserted_into_article(self):
        with session_scope(engine=TestDataAccess.engine) as session: 
            record = {'title':'title_1', 'sub_title':'sub_title_1', 'text':'text_1'}
            asserted = Article(**record)

            add_new_record(session, record)
            tested = session.query(Article).one()
            
            self.assertEqual(tested, asserted)

    def test_inserting_new_article_doesnt_get_inserted_into_article_log(self):
        with session_scope(engine=TestDataAccess.engine) as session: 
            record = {'title':'title_1', 'sub_title':'sub_title_1', 'text':'text_1'}
            asserted = []
            
            add_new_record(session, record)
            tested = session.query(ArticleOccurenceLog).all()

            self.assertEqual(tested, asserted)

    def test_inserting_existing_article_creates_rec_article_log_with_the_correct_datetime(self):
        with session_scope(engine=TestDataAccess.engine) as session: 
            record_1 = {'id':1, 'title':'title_1', 'sub_title':'sub_title_1', 'text':'text_1'}
            record_2 = {'title':'title_1', 'sub_title':'sub_title_1', 'text':'text_1'}
            insert_datetime_1 = datetime.datetime(year=2021, month=11, day=1)
            insert_datetime_2 = datetime.datetime(year=2021, month=11, day=2)
            add_new_record(session, record_1, insert_datetime_1)
            add_new_record(session, record_2, insert_datetime_2)

            article = Article(**record_1)
            asserted = ArticleOccurenceLog(**{'article':article,
                'insert_datetime':insert_datetime_2})

            tested = session.query(ArticleOccurenceLog).all()[0]

            self.assertEqual(asserted, tested)

    def test_inserting_existing_article_creates_one_rec_in_article_log(self):
        with session_scope(engine=TestDataAccess.engine) as session: 
            record_1 = {'id':1, 'title':'title_1', 'sub_title':'sub_title_1', 'text':'text_1'}
            record_2 = {'title':'title_1', 'sub_title':'sub_title_1', 'text':'text_1'}

            add_new_record(session, record_1)
            add_new_record(session, record_2)

            article = Article(**record_1)
            asserted = 1

            tested = len(session.query(ArticleOccurenceLog).all())

            self.assertEqual(asserted, tested)

suite = unittest.TestLoader().loadTestsFromTestCase(TestDataAccess)
unittest.TextTestRunner(verbosity=2).run(suite)

