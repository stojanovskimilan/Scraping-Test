import requests
import urllib
import re
from bs4 import BeautifulSoup
import pandas as pd
from collections import namedtuple
import itertools
from urllib.request import urlopen

requests.packages.urllib3.disable_warnings()

URLS = {'CPU':'https://www.newegg.com/p/pl?Submit=StoreIM&Category=34&PageSize=96',
'LAPTOP': 'https://www.newegg.com/PCs/EventSaleStore/ID-1837?N=100017489&PageSize=96',
'PC': 'https://www.newegg.com/p/pl?Submit=StoreIM&Category=228&PageSize=96',
'GADGETS': 'https://www.newegg.com/p/pl?N=100006940&PageSize=96',
'HEADPHONES': 'https://www.newegg.com/p/pl?Submit=StoreIM&Category=158&PageSize=96',
'TV': 'https://www.newegg.com/p/pl?Submit=StoreIM&Category=59&PageSize=96',
'MONITORS' : 'https://www.newegg.com/Gaming-Monitors/SubCategory/ID-3743?PageSize=96'}


def scrape_data(url):
    html = requests.get(url).text
    response = requests.get(url)
    soup = BeautifulSoup(html, 'html.parser')

    titles, prices, ratings_list, product_urls = ([] for i in range(4))

    for div in soup.find_all('div', {'class': 'item-cell'}):
        title = div.find('a', {'class': 'item-title'})
        titles.append(title.text)
        price = div.find('ul', {'class': 'price'})
        current_price = price.find('li', {'class': 'price-current'})

        prices.append(current_price.text.split('(')[0])
        ratings = div.find('a', {'class': 'item-rating'})
        if ratings is None:
            ratings_list.append(ratings)
        else:
            ratings_list.append(ratings['title'].split(' ')[2])

        a = div.find('a', {'class': 'item-img'})
        product_urls.append(a['href'])
    return titles, prices, ratings_list, product_urls


def get_sellers(product_urls):
    sellers = []
    for url in product_urls:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', {'class': 'product-seller no-border-bottom'})
        if div == None:
            sellers.append(None)
        else:
            a = div.find('a')
            sellers.append(a.text)

    return sellers


def get_description(product_url):
    html = requests.get(product_url).text
    soup = BeautifulSoup(html,'html.parser')
    div1 = soup.find('div', {'class': 'product-bullets'})
    ul = div1.find('ul')
    a = []
    if ul is not None:
        for e in ul:
            a.append(e.text)
    else:
        a.append(None)
    return a


