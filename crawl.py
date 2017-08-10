#! /usr/bin/python
'''
Crawl website.
'''

import urllib2
import re

def download(url, user_agent='wswp', num_retries=2):
    '''
    download(url, usrer_agent='wswp', num_retries=2)==>html string.
    '''
    print 'Downloading:', url
    headers = {'Userr-agent' : user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                #retry 5xx HTTP errors
                return download(url, user_agent, num_retries-1)
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


if __name__ == '__main__':
    crawl_sitemap('http://www.baidu.com')
