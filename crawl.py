#!/usr/bin/python3
import sys
from articles.spiders import spider
from scrapy.crawler import CrawlerProcess
import re
from urllib.parse import urlparse

url = sys.argv[1]
url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
valid_url = re.match(url_regex, url) is not None

words = sys.argv[2]
try:
    int(words)
    valid_no = True
except Exception:
    valid_no = False

if not valid_url:
    print("Please input a valid url e.g. 'http://example.com' ")
elif not valid_no:
    print("Please input a valid number of words to search for ")
else:
    def main_spider():
        process = CrawlerProcess(settings={'TELNETCONSOLE_ENABLED':False,'USER_AGENT':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125"})
        process.crawl(spider.ArticlesSpider, url=url, words=words)
        process.start() 
    main_spider()

    try:
        with open(f'{urlparse(url).netloc}.csv', "r") as f:
            print(f"\n\n\n{len(f.readlines())} articles scraped on {url}\n\n\n")       
    except Exception:
        print(f"\n\n\nNo articles found on {url}\n\n\n")        

