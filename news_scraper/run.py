import argparse
import logging
import time

from schedule import every, repeat, run_pending
import schedule

from news_scraper.scraper.scraper import retrieve_page, parse_articles
from news_scraper.data_access.data_access import session_scope, add_new_record
from news_scraper import db_uri

logger = logging.getLogger('__name__')

url='https://www.spiegel.de/international/'

def parse_args(func): 
    def wrapper(*args, **kwargs):
        parser = argparse.ArgumentParser()
        parser.add_argument('--url', '-u', help='Spiegel international news feed url.')
        arguments = parser.parse_args()  
        if arguments.url: 
            return_value = func(url=url, *args, **kwargs)
        else: 
            return_value = func(*args, **kwargs)
        return return_value
    return wrapper 

@parse_args
def job(url=url):
    '''
    Downloads html doc, parses it, saves data w.r.t business logic.
    '''
    try: 
        doc = retrieve_page(url)
        mapped_articles = parse_articles(doc)
        
        logger.debug('Number of article teasers: {}\n'.format(len(mapped_articles)))
        
        with session_scope(db_uri) as session:
            for article in mapped_articles: 
                add_new_record(session, article)
    
    except Exception as e: 
        logger.exception(e)

def run_job():
    schedule.every(15).minutes.do(job)
    while True:
        run_pending()
        time.sleep(1)


if __name__=='__main__': 
    run_job()
