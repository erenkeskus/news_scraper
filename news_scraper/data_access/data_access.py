from contextlib import contextmanager
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from news_scraper.data_access.models import Article, ArticleOccurenceLog
from news_scraper.data_access.models import metadata

logger = logging.getLogger(__name__)

def init_db(db_uri): 
    engine = create_engine(db_uri)
    metadata.create_all(bind=engine)
    return engine

@contextmanager
def session_scope(db_uri=None, engine=None):    
    if not engine: 
        engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.commit()
        raise
    finally:
        session.close()

def create_instance(session, article_data, update_time):
    '''
    Checks if article record is in db, returns an instance of a model accordingly
    Arguments: 
        session: a db session of type 'sqlalchemy.orm.Session'
        article data: a 'dict' with mapped article info
        updatetime: 'datetime.datetime' object mainly for unit tests. when None sit will
            be with server default replaced. 
    Returns: 
    rec either of 'Article' or 'ArticleOccurence' types instance
    '''
    rec = Article(**article_data)
    existing_article = retrieve_article(session, rec)
    if existing_article:
        logger.debug('Existing article: {}'.format(existing_article))
        rec = ArticleOccurenceLog(article_id=existing_article.id, 
            insert_datetime=update_time)
    return rec

def add_new_record(session, article_data, update_time=None): 
    '''
    Adds either Article or ArticleOccuranceLog record. 
    Arguments: 
        session: a db session of type 'sqlalchemy.orm.Session'
        article data: a 'dict' with mapped article info
        updatetime: 'datetime.datetime' object mainly for unit tests. when None sit will
            be with server default replaced. 

    '''
    rec = create_instance(session, article_data, update_time)
    logger.info('Saving: {}'.format(rec))
    return session.add(rec)

def retrieve_article(session, article):
    '''
    Retrieves article record from db. 
    Returns: 
        instance of 'Article' or None
    '''
    return  session.query(Article).filter_by(
                title=article.title,
                sub_title=article.sub_title,
                text=article.text
            ).one_or_none()