import argparse
import logging

from news_scraper.scraper.scraper import retrieve_page, parse_articles
from news_scraper.data_access.data_access import session_scope, add_new_record
from news_scraper import db_uri

logger = logging.getLogger('news_scraper.run')

def run(url='https://www.spiegel.de/international/'):
	'''
	Downloads html doc, parses it, saves data w.r.t business logic.
	'''
	try: 
		parser = argparse.ArgumentParser()
		parser.add_argument('--url', '-u', help='Spiegel international news feed url.')
		args = parser.parse_args()  
		if args.url: 
			url = args.url
		
		doc = retrieve_page(url)
		mapped_articles = parse_articles(doc)
		
		logger.debug('Number of article teasers: {}\n'.format(len(mapped_articles)))
		
		with session_scope(db_uri) as session:
			for article in mapped_articles: 
				add_new_record(session, article)
	
	except Exception as e: 
		logger.exception(e)

if __name__=='__main__': 
	run()

