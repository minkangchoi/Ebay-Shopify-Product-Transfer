import shopify
import requests
import urllib.parse

'''
    SHOPIFY:    https://accounts.shopify.com/store-login
        store name:     wpmore
        email:          soojoo2005@me.com
        password:       Gosoojoo1

    EBAY:       https://signin.ebay.com/signin/
        username: wpmore
        password: Gosoojoo
'''

shopify.ShopifyResource.clear_session()

API_KEY = '3c2a8b1b9f3fea800a8cf7917ffe18ec'
PASSWORD = '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'
API_VERSION = '2020-01'

shop_url = "https://%s:%s@widepeepohappy.myshopify.com/admin/api/%s" % (API_KEY, PASSWORD, API_VERSION)
shopify.ShopifyResource.set_site(shop_url)
         
shop = shopify.Shop.current

new = shopify.Product()
title = 'test'

enc = urllib.parse.quote(title)
r = requests.get(shop_url + '/products.json?title=' + enc)

if not r.json()['products']:

    # NEED title, decscription, media, pricing(price), charge tax on product, quantity (availible), weight
    new.title = title
    

    # CONSISTENT: charge tax on product, track quantity check, physical product check, 
    new.fulfillment_service = 'manual'
    new.inventory_management = 'shopify'

    success = new.save()
    
