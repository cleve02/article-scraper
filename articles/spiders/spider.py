
from bs4 import BeautifulSoup
from scrapy import Request, Spider
from scrapy import signals
from urllib.parse import urlparse
from scrapy.exceptions import CloseSpider
class ArticlesSpider(Spider):
    name = 'articles'

    IGNORED_EXTENSIONS = [
        # images
        'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
        'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

        # audio
        'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

        # video
        '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
        'm4a',

        # other
        'css', 'pdf', 'doc', 'exe', 'bin', 'rss', 'zip', 'rar',
    ]    

    def __init__(self, url=None, words=None, *args, **kwargs):
        super(ArticlesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.allowed_domains = [urlparse(url).netloc]
        self.words = words
        self.url = url

    def parse(self, response_):
        response = response_.body
        page = BeautifulSoup(response, "html.parser")
        
        try:
            with open(f'{urlparse(self.url).netloc}.csv','r+') as f:
                if len(f.readlines()) >= 10000:
                    raise CloseSpider('Scrape limit reached')
        except FileNotFoundError:
            pass

        try:
            words_list = page.body.text.split()
        except Exception:
            words_list = page.text.split()

        extension = response_.request.url.split('.')[-1] 
        if extension in self.IGNORED_EXTENSIONS: #unwanted extensions
            pass
        elif len(response_.request.url.split('.')) > 2 and urlparse(response_.request.url).netloc.split('.')[-3] != "www": #subdomains
            pass
        elif urlparse(response_.request.url).netloc.split('.')[-2] != urlparse(self.url).netloc.split('.')[-2]:
            pass
        else:
            if len(words_list) > int(self.words):
                with open(f'{urlparse(self.url).netloc}.csv','a+') as f:
                    with open(f'{urlparse(self.url).netloc}.csv','r+') as f:
                        if response_.request.url in f.read():
                            print("\nAlready scraped this URL\n")
                        else:
                            f.write(f"{response_.request.url},{len(words_list)}\n")

        links = page.find_all('a')  
        for link in links:
            try:
                url_to_follow = link['href']
                yield response_.follow(url_to_follow, callback=self.parse)
            except Exception:
                pass


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ArticlesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        # crawler.signals.connect(spider.spider_error, signal=signals.spider_error)  
        # crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)      
        return spider

    def spider_opened(self, spider):
        print(f"Starting scraper on {self.url}, words: {self.words}")
        

    # def spider_error(self, failure, response):
    #     print(f"GLOBAL ERROR: {failure} on Main Global Spider")

    # def spider_closed(self, spider):
    #     with open(f'{urlparse(self.url).netloc}.csv', "r") as f:
    #         print(f"\n\n\n{len(f.readlines())} articles scraped on {self.url}\n\n\n")
 


