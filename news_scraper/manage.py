from news_scraper import db_uri
from news_scraper.data_access.data_access import init_db
    
def initialize_db():
    init_db(db_uri)

if __name__=='__main__':
    initialize_db()