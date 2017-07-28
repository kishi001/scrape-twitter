# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 15:13:01 2017

@author: kishi
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import csv
import io
import pprint as pp


path_to_chromedriver ="C:\\Users\\kishi\\Downloads\\chromedriver_win32\\chromedriver"            #enter path of chromedriver
browser = webdriver.Chrome(executable_path = path_to_chromedriver)


url = input("Enter the url: ")  #eg: https://www.twitter.com/xyz/

#this function is to handle dynamic page content loading - using Selenium
def tweet_scroller(url):

    browser.get(url)
    
    #define initial page height for 'while' loop
    lastHeight = browser.execute_script("return document.body.scrollHeight")
    
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #define how many seconds to wait while dynamic page content loads
        time.sleep(3)
        newHeight = browser.execute_script("return document.body.scrollHeight")
        
        if newHeight == lastHeight:
            break
        else:
            lastHeight = newHeight
            
    html = browser.page_source

    return html


    
#function to handle/parse HTML and extract data - using BeautifulSoup    
def scrapper(url):
    
    #regex patterns
    url_finder = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    problemchars = re.compile(r'[\[=\+/&<>;:!\\|*^\'"\?%$@)(_\,\.\t\r\n0-9-—\]]')
    prochar = '[(=\-\+\:/&<>;|\'"\?%#$@\,\._)]'
    crp = re.compile(r'MoreCopy link to TweetEmbed Tweet|Reply')
    retweet = re.compile(r"(?<=Retweet:)(.*)(?=', u'R)")
    fave = re.compile(r"(?<=Like:)(.*)(?=', u'Liked)")
    wrd = re.compile(r'[A-Z]+[a-z]*')
    dgt = re.compile(r'\d+')    
    

    blog_list = []
     
    #set to global in case you want to play around with the HTML later   
    global soup    
    
    #call dynamic page scroll function here
    soup = BeautifulSoup(tweet_scroller(url), "html.parser")
    
    
        
    for i in soup.find_all('li', {"data-item-type":"tweet"}):
        user = (i.find('span', {'class':"username js-action-profile-name"}).get_text() if i.find('span', {'class':"username js-action-profile-name"}) is not None else "")
        link = ('https://twitter.com' + i.small.a['href'] if i.small is not None else "")
        date = (i.small.a['title'] if i.small is not None else "")
        popular = (i.find('div', {'class': "js-tweet-text-container"}).get_text().replace('\n','') if i.find('div', {'class': "js-tweet-text-container"}) is not None else "")
        text = (i.p.get_text().replace('\n','') if i.p is not None else "")
        popular_text = [i + ':' + j  if len(dgt.findall(popular)) != 0 else '' for i, j in zip(wrd.findall(crp.sub('', popular)), dgt.findall(popular))]
        
            
            #build dictionary to format data as key-pair value 
        blog_dict = {
        "header": "twitter_hashtag_" + url.rsplit('/',2)[1],
        "url": link,
        "user": user,
        "date": date,
        "popular": popular_text,
            #before text is stored URLs are removed - note: hash symbol is maintained to indicate hashtag term
        "blog_text": problemchars.sub(' ', url_finder.sub('', text)),
        "like_fave": (int(''.join(fave.findall(str(popular_text)))) if len(fave.findall(str(popular_text))) > 0 else ''),
        "share_retweet": (int(''.join(retweet.findall(str(popular_text)))) if len(retweet.findall(str(popular_text))) > 0 else '')
        }
        
        blog_list.append(blog_dict)            
    
        
            
    #call csv writer function and output file
    writer_csv_3(blog_list)
    
    return pp.pprint(blog_list[0:2])

    
    
#function to write CSV file
def writer_csv_3(blog_list):
    
    #uses group name from URL to construct output file name
    file_out = "twitter_hashtag_{page}.csv".format(page = url.rsplit('/',2)[1])
    
    with io.open(file_out, "w", encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile, lineterminator='\n', delimiter=',', quotechar='"')
    
        for i in blog_list:
            if len(i['blog_text']) > 0:
                newrow = i['header'], i['url'], i['user'], i['date'], i["popular"],i["blog_text"] ,i["like_fave"], i["share_retweet"]

                writer.writerow(newrow)                     
            else:
                pass
    
    
#main
if __name__ == "__main__":
    scrapper(url)