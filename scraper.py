#!/usr/bin/python

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')

import re
def re_scraper(html):
    results = {}
    for field in FIELDS:
        #results[field] = re.search('<tr id="places_%s__row".*?<td class="w2p_fw">(.*?)</td>' % field, html).groups()[0]
        results[field] = re.search('<tr id="places_{}__row".*?<td class="w2p_fw">(.*?)</td>'.format(field), html).groups()[0]
    return results

from bs4 import BeautifulSoup
def bs_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = {}
    for field in FIELDS:
        #results[field] = soup.find('table').find('tr', id='places_%s__row' % field).find('tr', class_='w2p_fw').text
        #results[field] = soup.find('table').find('tr', id='places_{}__row'.format(field)).find('tr', class_='w2p_fw').text
	tb = soup.find('table')
	tr = tb.find('tr', id='places_{}__row'.format(field))
	trclass = tr.find('tr', class='w2p_fw').text #fault!!!
	results[field] = trclass.text
    return results

import lxml.html
def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    results = {}
    for field in FIELDS:
        #results[field] = tree.cssselect('table > tr#places_%s__row > td.w2p_fw' % field)[0].text_content()
        results[field] = tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content()
    return results
