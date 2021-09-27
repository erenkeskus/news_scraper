import requests
from bs4 import BeautifulSoup

def retrieve_page(url): 
	response = requests.get(url=url)
	if response.ok: 
		return response.content

def parse_articles(document):
	'''
	This function parses an html doc and collects article information from it. 
	Returns -> articles_map (dict). contains a list of mapped article
	'''
	soup = BeautifulSoup(document, 'html.parser')
	articles_map = []
	inhalt = soup.find(id='Inhalt')
	articles = inhalt.find_all(attrs={'data-block-el':'articleTeaser', 'class':'z-10 w-full'})
	for article in articles: 
		title = articles[0].h2.a.get('title').strip()
		sub_title = articles[0].h2.a.span.text.strip()
		anchor = articles[0].a
		p = articles[0].find('p')
		text = p.span.text.strip()
		articles_map.append({'title':title, 'sub_title':sub_title, 'text':text})

	return articles_map



