# scrape-twitter

Scrape any twitter page using Selenium and BeautifulSoup in Python.

This program uses Selenium ChromeDriver to automatically browse the Twitter page and load data from dynamic scrolling. 
Once the pages are rendered the HTML is extracted and scraped through BeautifulSoup.

Note: It'll continue scraping until 

1) the end of feed is reached , 

2) by manual interruption i.e. killing the connection.


Requirements: Python 3.x, Selenium, bs4 module (if not installed in your python), Chrome Driver for Chrome browser (can use other drivers to run on other browsers as well.)
