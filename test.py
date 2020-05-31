import shopify
import requests
import urllib.parse

shopify.ShopifyResource.clear_session()

API_KEY = '3c2a8b1b9f3fea800a8cf7917ffe18ec'
PASSWORD = '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'
API_VERSION = '2020-01'

shop_url = "https://%s:%s@widepeepohappy.myshopify.com/admin/api/%s" % (API_KEY, PASSWORD, API_VERSION)

title = 'test'
enc = urllib.parse.quote(title)
r = requests.get(shop_url + '/products.json?title=' + enc)

inventoryItemId = r.json()['products'][0]['variants'][0]['inventory_item_id']

q = requests.get(shop_url + '/inventory_levels.json?inventory_item_ids=' + str(inventoryItemId))

locationId = q.json()['inventory_levels'][0]['location_id']

postobj = {  "location_id": locationId, "inventory_item_id": inventoryItemId, "available": 24}

x = requests.post(shop_url + '/inventory_levels/set.json', data = postobj)

print(x.json())
