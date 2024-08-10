import requests
from bs4 import BeautifulSoup
import sqlite3

# Fetch the webpage
url = 'https://avandmobile.com/product/samsung-galaxy-a10s-32g/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize lists to hold the data
titles = []
links = []
images = []
prices = []
description_info = []
additional_info = []
review_info = []
reviews_info = []

# Get all titles with h1 and h2 tags
for tag in soup.find_all(['h1', 'h2']):
    titles.append(tag.get_text(strip=True))
# print(titles)

# Get all links with a tag and href
for tag in soup.find_all('a', href=True):
    links.append(tag['href'])
# print(links)

# Get all images with img tag and src
for tag in soup.find_all('img', src=True):
    images.append(tag['src'])
# print(images)

# Get all prices
# Note: This assumes prices are in a specific class or pattern. Adjust the selector as needed.
for tag in soup.find_all("p",class_='stock'):
    prices.append(tag.get_text(strip=True))
# print(prices)

# Get all the information under specific li tags
li_classes = [
    'description_tab',
    'additional_information_tab',
    'review_p_tab_tab',
    'reviews_tab'
]

for li_class in li_classes:
    for tag in soup.find_all('li', class_=li_class):
        if li_class == 'description_tab':
            description_info.append(tag.get_text(strip=True))
            print(description_info)
        elif li_class == 'additional_information_tab':
            additional_info.append(tag.get_text(strip=True))
        elif li_class == 'review_p_tab_tab':
            review_info.append(tag.get_text(strip=True))
        elif li_class == 'reviews_tab':
            reviews_info.append(tag.get_text(strip=True))


# Store data in a text file
with open('scraped_data.txt', 'w', encoding='utf-8') as file:
    file.write("Titles:\n" + "\n".join(titles) + "\n\n")
    file.write("Links:\n" + "\n".join(links) + "\n\n")
    file.write("Images:\n" + "\n".join(images) + "\n\n")
    file.write("Prices:\n" + "\n".join(prices) + "\n\n")
    file.write("Description Info:\n" + "\n".join(description_info) + "\n\n")
    file.write("Additional Info:\n" + "\n".join(additional_info) + "\n\n")
    file.write("Review Info:\n" + "\n".join(review_info) + "\n\n")
    file.write("Reviews Info:\n" + "\n".join(reviews_info) + "\n")

# Store data in a SQLite database
conn = sqlite3.connect('scraped_data.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS titles (title TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS links (link TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS images (image_url TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS prices (price TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS description_info (info TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS additional_info (info TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS review_info (info TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS reviews_info (info TEXT)''')

# Insert data into tables
cursor.executemany('INSERT INTO titles (title) VALUES (?)', [(title,) for title in titles])
cursor.executemany('INSERT INTO links (link) VALUES (?)', [(link,) for link in links])
cursor.executemany('INSERT INTO images (image_url) VALUES (?)', [(image,) for image in images])
cursor.executemany('INSERT INTO prices (price) VALUES (?)', [(price,) for price in prices])
cursor.executemany('INSERT INTO description_info (info) VALUES (?)', [(info,) for info in description_info])
cursor.executemany('INSERT INTO additional_info (info) VALUES (?)', [(info,) for info in additional_info])
cursor.executemany('INSERT INTO review_info (info) VALUES (?)', [(info,) for info in review_info])
cursor.executemany('INSERT INTO reviews_info (info) VALUES (?)', [(info,) for info in reviews_info])

# Commit and close
conn.commit()
conn.close()

print("Data scraping and storage complete.")