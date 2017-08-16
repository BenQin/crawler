#! /usr/bin/python
'''
Crawl website.
'''

import urllib2
import re
import itertools
import urlparse
import robotparser
import datetime
import time


class Throttle(object):
    '''Add a delay between downloads to the same domain
    '''
    def __init__(self, delay):
        #amount of delay between downloads for each domain
        self.delay = delay
        #timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                #domain has ben accessed recently, so need to sleep
                time.sleep(sleep_secs)
        #update the last accessed time
        self.domains[domain] = datetime.datetime.now()


def download(url, user_agent='wswp', proxy=None, num_retries=2):
    '''
    download(url, usrer_agent='wswp', num_retries=2)==>html string.
    '''
    print 'Downloading:', url
    headers = {'Userr-agent' : user_agent}
    request = urllib2.Request(url, headers=headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme : proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                #retry 5xx HTTP errors
                return download(url, user_agent, proxy, num_retries-1)
    return html


def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    print 'links length', len(links)
    # download each link
    for link in links:
        html = download(link)
        # scrape html here
        # ...

def crawl_id_traverse():
    max_errors = 5
    num_errors = 0
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/%d' % page
        html = download(url)
        if html is None:
	        num_errors += 1
	        if num_errors == max_errors:
	            break
        else:
	        num_errors = 0
	        #print html

def link_crawler(seed_url, link_regex, user_agent='GoodCrawler', max_depth=2):
    '''Crawl from the given seed URL following links matched by link_regex
    '''
    rp = robotparser.RobotFileParser()
    link = urlparse.urljoin(seed_url, 'robots.txt')
    rp.set_url(link)
    rp.read()
    crawl_queue = [seed_url]
    seen = {seed_url : 0} 
    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            html = download(url)
            depth = seen[url]
            if depth != max_depth:
                for link in get_links(html):
                    if re.search(link_regex, link):
                        link = urlparse.urljoin(seed_url, link)
                        if link not in seen:
                            seen[link] = depth + 1
                            crawl_queue.append(link)
        else:
            print 'Blocked by robots.txt:', url

def get_links(html):
    '''Return a list of links from html
    '''
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


if __name__ == '__main__':
    crawl_sitemap('http://www.baidu.com')
