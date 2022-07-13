from requests import get
import pandas as pd
import csv
import ast
import tzlocal
from collections import ChainMap
from datetime import datetime
from operator import itemgetter

API_KEY = "VARJVSQQS61AM3ME598B131P4HNPR1VDUI"
address = "0x1f12ed3F2e7e896EdAd48bA568aEa06bD6Ea9d4f"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18
def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url
def get_transactions_name(address):
    transactions_url = make_api_url("account", "tokennfttx", address, startblock=0, endblock=99999999, page=1,
                                    offset=10000, sort="asc")
    response = get(transactions_url)
    data = response.json()['result']
    transactions_price_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1,
                                          offset=10000, sort="asc")
    response_price = get(transactions_price_url)
    data_price = response_price.json()['result']
    transactions_price_sale_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999,
                                               page=1, offset=10000, sort="asc")
    response_price_sale = get(transactions_price_sale_url)
    data_price_sale = response_price_sale.json()['result']
    keys = ['timeStamp', 'hash', 'tokenName', 'to']
    res = []
    for dict1 in data:
        result = dict((k, dict1[k]) for k in keys if k in dict1)
        res.append(result)
    keys = ['hash', 'to', 'value']
    res2 = []
    for dict2 in data_price:
        result = dict((k, dict2[k]) for k in keys if k in dict2)
        res2.append(result)
    keys = ['hash', 'to', 'value']
    res3 = []
    for dict2 in data_price_sale:
        result = dict((k, dict2[k]) for k in keys if k in dict2)
        res3.append(result)
    hash = {row['hash'] for row in res}
    unique = []
    for unique_hash in hash:
        unique.append(dict(ChainMap(*(row for row in res if row['hash'] == unique_hash))))

    for index, lst1 in enumerate(unique):
        for lst2 in res2:
            if lst2["hash"] == lst1["hash"]:
                unique[index]["value"] = lst2["value"]
                break
    for index, lst1 in enumerate(unique):
        for lst2 in res3:
            if lst2["hash"] == lst1["hash"]:
                unique[index]["value"] = lst2["value"]
                break
    for item in unique:
        if item.get('to'):
            if item.get('to').lower() == address.lower():
                item["to"] = "Buy"
            else:
                item["to"] = "Sell"
    for item1 in unique:
        item1['timeStamp'] = datetime.fromtimestamp(int(item1['timeStamp']))
        item1['value'] = int(item1['value']) / ETHER_VALUE

    unique.sort(key=itemgetter('timeStamp'), reverse=True)
    unique = [{k: v for k, v in d.items() if k != 'hash'} for d in unique]

    commonkeys = ['timeStamp', 'to', 'tokenName', 'value']
    with open('test_brandon.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=commonkeys)
        writer.writeheader()
        writer.writerows(unique)

address = "0x1f12ed3F2e7e896EdAd48bA568aEa06bD6Ea9d4f"
get_transactions_name(address)

    unique = [{k: v for k, v in d.items() if k != 'hash'} for d in unique]
    unique['transaction'] = unique['to']
    del unique['to']
