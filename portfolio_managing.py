
import argparse
from bs4 import BeautifulSoup
import itertools
import threading
import time
import sys
import re

import requests

"""
This is for checking Vietnamese Stock Market result

built on requests and Beautiful Soup 4

"""

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rWe are loading your data please wait ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('-----------------------------------------------------------------     \n')


done = False

def get_stock(stock_lists):
    prefix_link = "http://www.cophieu68.vn/snapshot.php?id="
    stock_prices = []
    stock_changes = []
    stock_changes_percentage = []
    for stock_name in stock_lists:
        link = prefix_link + stock_name
        page_stock_data = requests.get(link).text
        raw_stock_data = BeautifulSoup(page_stock_data, 'html.parser')
        price = raw_stock_data.find(id='stockname_close').text
        # For processing the stock price change
        change = raw_stock_data.find(id='stockname_change').text
        change = re.findall('[0-9]',change)
        price_change = '.'.join(change[:2]) + change[3]
        percent_change = ','.join(change[3:]) + '%'
        stock_prices.append(price)
        stock_changes.append(price_change)
        stock_changes_percentage.append(percent_change)
    stock_data = list(zip(stock_lists, stock_prices, stock_changes, stock_changes_percentage))
    return stock_data
    
def get_bitcoin():
    bitcoin_news = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()
    bitcoin_price = bitcoin_news['bpi']['USD']['rate']
    return bitcoin_price
    
def get_ether():
    ether_page_data = requests.get('https://ethereumprice.org').text
    raw_eth_data = BeautifulSoup(ether_page_data,'html.parser')
    ether_price_data = raw_eth_data.find_all('span', {'class':'rp'})
    ether_price = ether_price_data[0].text
    price_change_24h =  ether_price_data[1].text
    percent_change_24h = ether_price_data[4].text
    return '  |  '.join([ether_price, price_change_24h + '%', percent_change_24h])

def main():
    parser = argparse.ArgumentParser(description='Process a username.')
    parser.add_argument( '--stock', nargs='+', type=str, help='Input your list of stock')
    args = parser.parse_args()
    stock_lists = args.stock
    coin_news = ("\nHere is your investing news\n"
                 "-----------------------------------------------------------------\n"
                 "The price of your beloved bitcoin\n{0}\n"
                 "The price of your beloved ethereum\n{1}".format(get_bitcoin(), get_ether()))

    if stock_lists:
        stock_news = ["Price of {0} : {1} | {2} | {3}".format(name, price, change, percent) for name, price, change, percent in get_stock(stock_lists)]
        print(coin_news)
        for new in stock_news:
            print(new)
    else:
        print(coin_news)        


if __name__ == '__main__':
    t = threading.Thread(target=animate)
    t.start()
    main()
    done = True
