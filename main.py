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
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome("C:\ie\chromedriver.exe", options=options)
    driver.get(url)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.set_window_position(-10000, 0)
    time.sleep(0.5)
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += 300
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")

    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find('ol', attrs={'id': 'prices'})
    # try:
    for row in table.find_all('li', attrs={'class': 'card js-product-card has-merchant-selection'}):
        quote = {}
        quote['shop'] = row.get('id')
        quote['shopName'] = row.find('div', {'class': 'shop-name'}).text
        quote['price'] = row.find('strong', {'class': 'dominant-price'}).text
        quote['available'] = row.find('p', {'class': 'availability'}).text
        quotes.append(quote)
    driver.quit()
    flag = 1
    first = 0
    hdprice = 0
    try:
        for item in quotes:
            if ('Άμεση παραλαβή' in item['available'] and flag == 1):
                print(item['shopName'], float(item['price'][:5].replace(',', '.')))
                first = float(item['price'][:5].replace(',', '.'))
                flag = 0
            if (item['shop'] == 'shop-1503'):
                hdprice = float(item['price'][:5].replace(',', '.'))
                print(item['shopName'], hdprice)
        delta = hdprice - first
        print(delta, hdprice, first)
        if (delta > 0):
            msrp, lowest, step = [float(s) for s in
                                  input('Enter Msrp  lowestPrice and Step seperated with spaces: ').split()]
            if first <= lowest:
                print('You cant be first you price gets the lowest ', lowest)
            elif first > msrp:
                print('the price is at msrp ', msrp)
            elif first <= msrp and hdprice >= lowest:
                print('the price is ', first - step)
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