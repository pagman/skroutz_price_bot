import requests
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from googlesearch import search
import csv
class Product:
  def __init__(self, uid, title, price, availability, directlink):
    self.uid = uid
    self.title = title
    self.price = price
    self.availability = availability
    self.directlink = directlink
ptable = []

def findprice(url):
    #URL = "https://www.skroutz.gr/s/23566446/Xiaomi-Mi-True-Wireless-Earphones-2-Basic-Bluetooth-Handsfree-%CE%9B%CE%B5%CF%85%CE%BA%CF%8C.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    quotes = []  # a list to store quotes
    table = soup.find('div', {'class': 'shop cf'})
    # print(table)
    table = soup.find('ol', attrs={'id': 'prices'})
    # print(table)
    try:
        for row in table.find_all('li', attrs={'class': 'card js-product-card has-merchant-selection'}):
            quote = {}
            quote['price'] = row.find('div', {'class': 'pre-blp content-placeholder'}).text
            quote['shop'] = row.get('id')
            quotes.append(quote)
        i = 0
        hd = 0
        for item in quotes:
            if (i == 0):
                first = float(item['price'][:5].replace(',', '.'))
                #print('First', item['shop'], first)
            if (item['shop'] == 'shop-1503'):
                hd = float(item['price'][:5].replace(',', '.'))
                #print('Hellas Digital', item['shop'], float(item['price'][:5].replace(',', '.')))
            i = i + 1
        delta = hd - first

        if (delta>0):
            msrp, lowest, step = [float(s) for s in input('Enter Msrp  lowestPrice and Step seperated with spaces: ').split()]
            if first <= lowest:
                print('You cant be first you price gets the lowest ', lowest)
            elif first > msrp:
                print('the price is at msrp ', msrp)
            elif first <= msrp and hd >= lowest:
                print('the price is ', first-step)
        if delta == 0:
            print('You are first already')
        if delta < 0:
            print('You dont have this product at Skroutz but others do')
    except: # catch *all* exceptions
       e = sys.exc_info()[0]
       #print(e)
def main():
    url = 'http://www.hellasdigital.gr/xmldatafeed.php?format=skroutz'
    document = requests.get(url)
    soup = BeautifulSoup(document.content, "lxml-xml")
    for paragraph in soup.find_all('product'):
        ptable.append(Product(paragraph.uid.string, paragraph.title.string, paragraph.price.string, paragraph.availability.string, paragraph.directlink.string))

    for x in range(205):
        #print(ptable[x].title)
        query = ptable[x].title + ' ' + 'skroutz'
        for j in search(query, tld="gr", num=1, stop=1, pause=2):
            if ('https://www.skroutz.gr/s/' in j):
                print(j, x, 'from ', len(ptable))
                findprice(j)


if __name__ == "__main__":
    main()