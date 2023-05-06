import requests
from bs4 import BeautifulSoup
import csv

url_template = 'https://phongtro123.com/tinh-thanh/ha-noi?page={page}'

with open('phongtro2.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # writer.writerow(['Price',  'District', 'Ward', 'time', 'Area'])
    listRoom=[]
    for page in range(170):
        # Fetch the next page
        response = requests.get(url_template.format(page=str(page+105)))
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all rooms on the page
        rooms = soup.find('ul', {'class': 'post-listing clearfix'})
        rooms=rooms.find_all('li')
        print(rooms)
        for i in rooms:
         room_link1 = i.find('a', class_='clearfix')
         print(room_link1['href'])
         room_response = requests.get('https://phongtro123.com' + room_link1['href'])
         # room_response = requests.get('https://phongtro123.com/tinh-thanh/ha-noi/cho-thue-nha-tro-phong-tro-gia-re.html')
         soup = BeautifulSoup(room_response.content, 'html.parser')
         soupShortItem = soup.find('div', class_='post-attributes')
         if(soupShortItem==None):
             break
         # Extract the data for the room
         price = soupShortItem.find('div', class_='item price').find('span').text
         area = soupShortItem.find('div', class_='item acreage').find('span').text
         listAddress = soup.find('address', class_='post-address').text
         listAddress = listAddress.split(',')
         if len(listAddress) < 3:
             break
         district = listAddress[len(listAddress) - 2]
         ward = listAddress[len(listAddress) - 3]
         time = soup.find('table', class_='table').find_all('tr')
         time = time[5].find('time').text
         time = time[len(time) - 10:]
         print(time)

         writer.writerow([price, district, ward, time, area])
         # Move on to the next page

        # Process the rooms on the page



