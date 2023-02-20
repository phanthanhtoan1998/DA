import requests
from bs4 import BeautifulSoup
import csv

url_template = 'https://homedy.com/cho-thue-nha-tro-phong-tro-ha-noi/p{page}'
page = 1

with open('rooms.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Price',  'District', 'Ward', 'time', 'Area'])

    while True:
        # Fetch the next page
        response = requests.get(url_template.format(page=page))
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all rooms on the page
        rooms = soup.find_all('div', {'class': 'product-item'})

        # If there are no more rooms, break out of the loop
        if not rooms:
            break

        # Process the rooms on the page
        for room in rooms:
            # Follow the link to the room's page
            room_link1=room.find('a',class_='thumb-image')
            print(room_link1['href'])
            room_response = requests.get('https://homedy.com'+room_link1['href'])
            soup = BeautifulSoup(room_response.content, 'html.parser')
            soupShortItem=soup.find_all('div', class_='short-item')
            if len(soupShortItem)==1 or len(soupShortItem)>3:
                break
            # Extract the data for the room
            price = soupShortItem[0].find('strong').find('span').text
            area = soupShortItem[1].find('strong').find('span').text
            listAddress = soup.find('div', class_='address').find_all('span')
            if len(listAddress)<3:
                break
            district = listAddress[len(listAddress)-2].text
            ward =listAddress[len(listAddress)-3].text
            listProductInfo = soup.find('div', {'class': 'product-info'}).find_all('div')
            time=listProductInfo[0].find('p',class_='code').text
            writer.writerow([price , district, ward, time, area])

        # Move on to the next page
        page += 1
