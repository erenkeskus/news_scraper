from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from news_scraper.data_access.models import Article, ArticleOccurenceLog
from news_scraper.data_access.models import metadata


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
    rec = Article(**article_data)
    existing_article = retrieve_article(session, rec)
    if existing_article: 
        rec = ArticleOccurenceLog(article_id=existing_article.id, 
            insert_datetime=update_time)
    return rec

def add_new_record(session, article_data, update_time=None): 
    rec = create_instance(session, article_data, update_time)
    return session.add(rec)

def retrieve_article(session, article):
    return  session.query(Article).filter_by(
                title=article.title,
                sub_title=article.sub_title,
                text=article.text
            ).one_or_none()

if __name__=='__main__': 
    init_db('sqlite:///news.db')
    with session_scope('sqlite:///news.db') as session: 
        print(session.query(Article).all())
