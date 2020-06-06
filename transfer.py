#!/usr/bin/env python

import shopify
import requests
import urllib
import base64
import sys
from bs4 import BeautifulSoup

############ SETUP FOR USE
print('Enter Shopify shop name:')
SHOP_NAME = input()

print('Enter Shopify API Key:')
API_KEY = input()

print('Enter Shopify Application Password:')
PASSWORD = input()

print('Enter Ebay store page link:')
ebayURL = input()

############ SHOPIFY LOGIN
shopify.ShopifyResource.clear_session()
API_VERSION = '2020-01'

shop_url = "https://%s:%s@%s.myshopify.com/admin/api/%s" % (API_KEY, PASSWORD, SHOP_NAME, API_VERSION)
shopify.ShopifyResource.set_site(shop_url)

shop = shopify.Shop.current

############ EBAY SETUP
fp = urllib.request.urlopen(ebayURL)
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()

soup = BeautifulSoup(mystr, 'html.parser')

r5 = soup.find_all('li', class_='s-item')

i = 0
for product in r5:
    print('Product number: ', i)
    i += 1

    r6 = product.div.find('div', class_='s-item__info clearfix')
    link = r6.a['href']

    #price
    r7 = r6.find('div', class_='s-item__details clearfix')
    r8 = r7.find('div', class_='s-item__detail s-item__detail--primary')
    price = r8.string
    price = price[1:]
    print('price: $', price)

    productPage = urllib.request.urlopen(link)
    mybytes1 = productPage.read()

    mystr1 = mybytes1.decode("utf8")
    productPage.close()

    soupP = BeautifulSoup(mystr1, 'html.parser')

    s1 = soupP.body.find('div', id='CenterPanelDF')
    s2 = s1.div.div.find('div', id='CenterPanelInternal')

    # child for price and title
    s3 = s2.find('div', id='LeftSummaryPanel') 
    s4 = s3.find('div', class_='vi-swc-lsp')
    s5 = s4.find('span', class_='u-dspn')
    title = s5.string
    print('title: ', title)

    # path for image
    p1 = s2.find('div', id='PicturePanel')
    p2 = p1.find('div', class_='pp-ic pp-ic300')
    search = p2.style.string

    start = search.find('url("') + len('url("')
    end = search.find('");')
    imgurl = search[start:end]
    imgurl = imgurl.replace('225', '1600')
    print('image source: ', imgurl)

    # path for description
    iframe = soupP.find('iframe')['src']
    iframe = iframe.replace('amp;', '')

    result2 = requests.get(iframe)
    descHTML = result2.text
    print('description obtained')

    ########################### SHOPIFY #############################
    new = shopify.Product()

    enc = urllib.parse.quote(title)
    r = requests.get(shop_url + '/products.json?title=' + enc)

    # Handle errors
    if r.status_code == 401 or r.status_code == 400:
        print(r)
        print('ERROR: Invalid Shopify credentials. Please check if shop name, API key, and password are correct!')
        exit(1)

    if not r.json()['products']:

        # NEED title, decscription, media, pricing(price), charge tax on product, quantity (availible), weight
        new.title = title
        new.body_html = descHTML
        new.variants = new.variants = [{'price' : float(price)}]
        new.images = [{'src' : imgurl}]

        success = new.save()

        print('PRODUCT UPLOADED TO SHOPIFY')
    
print('Transfer Complete!')
