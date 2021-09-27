import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def retrieve_page(url): 
    response = requests.get(url=url)
    if response.ok: 
        return response.content
    else: 
        logger.warning('Response not ok. response code: '.format(response.status_code))
        return None

def parse_articles(document):
    '''
    This function parses an html doc and collects article information from it. 
    Returns -> articles_map (dict). contains a list of mapped article
    '''
    try: 
        soup = BeautifulSoup(document, 'html.parser')
        articles_map = []
    
        inhalt = soup.find(id='Inhalt')
        articles = inhalt.find_all(attrs={'data-block-el':'articleTeaser', 'class':'z-10 w-full'})
        for article in articles: 
            title = article.h2.a.get('title').strip()
            sub_title = article.h2.a.span.text.strip()
            p = article.find('p')
            text = p.span.text.strip()
            articles_map.append({'title':title, 'sub_title':sub_title, 'text':text})
    except Exception as e: 
        logger.exception(e)
        raise

    return articles_map



