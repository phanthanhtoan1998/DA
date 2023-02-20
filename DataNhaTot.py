import requests
from bs4 import BeautifulSoup
import csv
import threading

def scrape_page(page_num, data):
    # Send a request to the URL for a specific page
    url = f'https://www.nhatot.com/thue-phong-tro-ha-noi?page={page_num}'
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the relevant elements and extract the information
    houses = soup.find_all('div', class_='item')
    for house in houses:
        district = house.find('div', class_='item-area').text.strip()
        posting_time = house.find('div', class_='item-posting-time').text.strip()
        area = house.find('div', class_='item-acreage').text.strip()
        interior_condition = house.find('div', class_='item-furniture').text.strip()
        price = house.find('div', class_='item-price').text.strip()
        data.append([district, posting_time, area, interior_condition, price])

def scrape_all_pages(num_pages):
    data = []
    threads = []

    # Create a separate thread for each page to be scraped
    for page_num in range(1, num_pages + 1):
        thread = threading.Thread(target=scrape_page, args=(page_num, data))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete before continuing
    for thread in threads:
        thread.join()

    # Save the data to a CSV file
    with open('houses.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['District', 'Posting Time', 'Area', 'Interior Condition', 'Price'])
        writer.writerows(data)

if __name__ == '__main__':
    num_pages = 10  # Change this to the number of pages you want to scrape
    scrape_all_pages(num_pages)
