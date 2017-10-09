
import argparse
from bs4 import BeautifulSoup
import itertools
import threading
import time
import sys

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
    for stock_name in stock_lists:
        link = prefix_link + stock_name
        page_stock_data = requests.get(link).text
        raw_stock_data = BeautifulSoup(page_stock_data, 'html.parser')
        price = raw_stock_data.find(id='stockname_close').text
        stock_prices.append(price)
    stock_data = list(zip(stock_lists, stock_prices))
    return stock_data
    
def get_bitcoin():
    bitcoin_news = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()
    bitcoin_price = bitcoin_news['bpi']['USD']['rate']
    return bitcoin_price
    
def get_ether():
    ether_page_data = requests.get('https://ethereumprice.org').text
    raw_eth_data = BeautifulSoup(ether_page_data,'html.parser')
    ether_price = raw_eth_data.find_all('span', {'class':'rp'})[0].text
    return ether_price

def main():
    parser = argparse.ArgumentParser(description='Process a username.')
    parser.add_argument('stock_lists', nargs='+', type=str, help='Input your list of stock')
    args = parser.parse_args()
    stock_lists = args.stock_lists
    coin_news = ("\nHere is your investing news\n"
                 "-----------------------------------------------------------------\n"
                 "The price of your beloved bitcoin\n{0}\n"
                 "The price of your beloved ethereum\n{1}".format(get_bitcoin(), get_ether()))
    if stock_lists:
        stock_news = ["Here is the price of {0} : {1} ".format(name, price) for name, price in get_stock(stock_lists)]
    print(coin_news)
    for new in stock_news:
        print(new)        


if __name__ == '__main__':
    t = threading.Thread(target=animate)
    t.start()
    main()
    done = True
