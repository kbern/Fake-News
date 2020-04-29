#import time
import re
import json
import pandas as pd
#import requests
#from bs4 import BeautifulSoup

import newspaper

#DEFINE ARTICLE PARSER

def parse_article(scraped_page):
    #if len(scraped_page.html) <= 0 or len(scraped_page.url) <= 0:
     #   return None

    try:
        article = newspaper.Article(scraped_page)
        article.download()
        print(article.html)
        #article.parse()
        
    except Exception:
        print("Something went wrong parsing")
        return None

    if len(article.text) <= 40: #do we need to keep this?
        return None

    return {
        'batch': 2,
        #'scraped_page_id': article.id,
        'url': article.url,
        #'scraped_at': article.updated_at,
        'title': article.title,
        'content': article.text,
        'authors': ', '.join(article.authors),
        'keywords': ', '.join(article.keywords),
        'meta_keywords': article.meta_keywords,
        'meta_description': article.meta_description,
        'tags': ', '.join(article.tags),
        'summary': article.summary
    }

#SCRAPE ARTICLES

#url = "https://www.bridgemi.com/michigan-truth-squad/truth-squad-schuette-says-calley-failed-michigan-deserted-gop-and-trump"
#parse_article(url)

#bridgemi_paper = newspaper.build("https://www.bridgemi.com/michigan-truth-squad")

for scraped in bridgemi_paper.articles:
    print(article.url)
#    parse_article(scraped.url)

#cnn_article = cnn_paper.articles[0]
#cnn_article.download()
#cnn_article.parse()
#cnn_article.nlp()



#GET TAGS

from lxml import html

from newspaper import Article

#bridgemi

#1
#url = "https://www.bridgemi.com/michigan-truth-squad/truth-squad-schuette-says-calley-failed-michigan-deserted-gop-and-trump"

#2
#url = "https://www.bridgemi.com/michigan-truth-squad/truth-squad-does-bill-schuette-care-if-sick-people-can-get-insurance"

#3
#url = "https://www.bridgemi.com/michigan-truth-squad/who-approved-switch-flint-river-states-answers-draw-fouls"

#4
#url = "https://www.bridgemi.com/michigan-truth-squad/truth-squad-does-bill-schuette-care-if-sick-people-can-get-insurance"
# - STRONG etc. in bold

#leadstories
url = "https://hoax-alert.leadstories.com/3470237-fake-news-trapeze-artist-with-diarrhea-shits-on-23-people.html"


article = Article(url)

article.download()

#print(article.html)

h = html.fromstring(article.html)

#bridgemi
#1 - works
#print(h.xpath('//div[@class="ts-call__details"]/node()')[-1])

#2 - works?
#print(h.xpath('//p[@dir="ltr"]/node()'))

#3 - truthtable, works
#print(h.xpath('//td[@class="regular_foul"]/node()')[0])

#4 - doesnt work
#print(h.xpath('//span[@dir="ltr"]/node()'))

#<p dir="ltr"><span id="docs-internal-guid-64ec6c76-7fff-7a56-3565-a6802a067bda">
#For these reasons, Truth Squad finds the Michigan Republican Party’s ad to be </span><strong>FOUL</strong>.</p>

#<p dir="ltr"><span id="docs-internal-guid-f82ae48d-7fff-751f-3a0a-fd99e0fef6e3">
#We rate the claim </span><strong>misleading.</strong></p>
     

#leadstories

title = h.xpath('//title/node()')
print(title)

mylist = []
for i in range(0, 1):
    fw = title[i].split(":")
    fw_ = fw[0]
    print(fw_) #here w.o. ''
    mylist.append(fw_) 

print(mylist) #here w. ''



#import lxml.html
#t = lxml.html.parse(url)
#print(t.find(".//title").text)

#print(re.findall("([A-Z]+)", h.xpath('//title/node()')))
#print(re.findall("([A-Z]+)", h))



