#!/usr/bin/python

import time
import download
import re
import scraper

NUM_ITERATIONS = 1000
html = download.download('http://example.webscraping.com/places/default/view/China-47')
for name, scrp in [('RE', scraper.re_scraper), ('Lxml', scraper.lxml_scraper), ('BS', scraper.bs_scraper)]:
    start = time.time()
    for i in range(NUM_ITERATIONS):
        if scrp == scraper.re_scraper:
            re.purge()
        result = scrp(html)
        assert(result['area'] == '9,596,960 square kilometres')
    end = time.time()
    print '%s: %.2f seconds' % (name, end - start)
