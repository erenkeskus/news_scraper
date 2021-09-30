# news_scraper
This is a schedulable console app which scrapes the news feed of a given news source, saves the data, and updates it with the corresponding timestamp.

To run the crawler do the following: 
After cloning the repository navigate to the root of the repo in command shell. 

Build the image: 
docker build -t news_scraper:0.1 .

Create db: 
docker run --rm --env-file .env -v scraper_vol:/code/news_scraper news_scraper:0.1 python /code/news_scraper/manage.py

Create and run the container:
docker run --name scraper -d -v scraper_vol:/code/news_scraper --restart always --env-file .env news_scraper:0.1 run-job -u https://www.spiegel.de/international/
