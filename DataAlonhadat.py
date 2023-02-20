from bs4 import BeautifulSoup
import requests
from csv import writer

with open('housing.csv', 'a', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    # header = ['Price',  'District', 'Ward', 'Area']
    # thewriter.writerow(header)
    listCsv = []
    a=15
    for i in range(9867):
        print(str(i+a))
        linkurlalonhadat = 'https://alonhadat.com.vn/nha-dat/cho-thue/phong-tro-nha-tro/1/ha-noi/trang--'+str(i+a)+'.html'
        linkalonhadatpage = requests.get(linkurlalonhadat)
        soudalonhadat = BeautifulSoup(linkalonhadatpage.content, 'html.parser')
        finddivcontentitems=soudalonhadat.find('div',class_='content-items')
        hrefalonhadats=finddivcontentitems.find_all('div',class_='content-item')

        for hrefalonhadat in hrefalonhadats:
         testNone=hrefalonhadat.find('a',class_='vip')
         if(testNone==None):
             testNone = hrefalonhadat.find('a')
         url = 'https://alonhadat.com.vn'+testNone['href']
         print(url)
         page = requests.get(url)
         soud = BeautifulSoup(page.content, 'html.parser')
         # timeString=soud.find('span',class_='date').text
         # time=timeString[10:]
         classCssPrice = soud.find('span', class_='price')
         price = classCssPrice.find('span', class_='value').text
         classCssArea = soud.find('span', class_='square')
         area = classCssArea.find('span', class_='value').text
         classCssAddress = soud.find('div', class_='address')
         address = classCssAddress.find('span', class_='value').text
         addressList=address.split(',')
         if(len(addressList)<3):
             break
         saveCsv = [price,addressList[len(addressList)-2], addressList[len(addressList)-3], area]
         thewriter.writerow(saveCsv)