import sqlite3
import requests
from bs4 import BeautifulSoup

# Fetch the webpage
urls = ["https://avandmobile.com/product/samsung-galaxy-a10s-32g/",
        "https://www.ecell.ir/product/apple-watch-45mm-greenlion-hd-glass/",
        r"http://mobileisatis.ir/product/%da%af%d9%88%d8%b4%db%8c-%d8%a7%d9%be%d9%84-%d9%85%d8%af%d9%84-apple-iphone-13-128gb/"
        ]


# lists to hold the data
titles = []
links = []
images = []
prices = []
description_info = []
additional_info = []
procon_info = []
reviews_info = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
   
    # Get all the titles with h1 tag
    for tag in soup.find_all(["h1"]):
        titles.append(tag.get_text(strip=True))
# print(titles)
    # Get all links with a tag and href
    for tag in soup.find_all("a", href=True):
        links.append(tag['href'])
# # print(links)

# # Get all images with img tag and src
    for tag in soup.find_all('img', src=True):
        images.append(tag['src'])
# print(images)

# # Get all prices
    stock_tags = soup.find_all("p",class_='stock')
    price_tags = soup.find_all("p", class_='price')
    for tag in price_tags:
    prices.append(tag.get_text(strip=True))

    print(prices)

# # Get all the information under specific id
# div_ids = {
#     'tab-description': description_info,
#     'tab-additional_information': additional_info,
#     'tab-review_p_tab': procon_info,
#     'tab-reviews': reviews_info
# }

# for div_id, info_list in div_ids.items(): # to access the two parametes in the object
#     div = soup.find('div', id=div_id) #loops over description
#     if div:
#         info_list.append(div.get_text(strip=True))
#         print(info_list)

# # Store data in a text file
# with open('scraped_data-2.txt', 'w', encoding='utf-8') as file:
#     file.write("Titles:\n" + "\n".join(titles) + "\n\n") #---> tupols to strings
#     file.write("Links:\n" + "\n".join(links) + "\n\n")
#     file.write("Images:\n" + "\n".join(images) + "\n\n")
#     file.write("Prices:\n" + "\n".join(prices) + "\n\n")
#     file.write("Description Info:\n" + "\n".join(description_info) + "\n\n")
#     file.write("Additional Info:\n" + "\n".join(additional_info) + "\n\n")
#     file.write("Pro Con Info:\n" + "\n".join(procon_info) + "\n\n")
#     file.write("Reviews Info:\n" + "\n".join(reviews_info) + "\n")

# # Store data in a SQLite database
# conn = sqlite3.connect('scraped_data-2.db')
# cursor = conn.cursor()

# # Create tables
# cursor.execute('''CREATE TABLE IF NOT EXISTS titles (title TEXT)''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS links (link TEXT)''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS images (image_url TEXT)''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS prices (price TEXT)''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS description_info (info TEXT)''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS additional_info (info TEXT)''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS procon_info (info TEXT)''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS reviews_info (info TEXT)''')

# # Insert data into tables
# cursor.executemany('INSERT INTO titles (title) VALUES (?)', [(title,) for title in titles])
# cursor.executemany('INSERT INTO links (link) VALUES (?)', [(link,) for link in links])
# cursor.executemany('INSERT INTO images (image_url) VALUES (?)', [(image,) for image in images])
# cursor.executemany('INSERT INTO prices (price) VALUES (?)', [(price,) for price in prices])
# cursor.executemany('INSERT INTO description_info (info) VALUES (?)', [(info,) for info in description_info])
# cursor.executemany('INSERT INTO additional_info (info) VALUES (?)', [(info,) for info in additional_info])
# cursor.executemany('INSERT INTO procon_info (info) VALUES (?)', [(info,) for info in procon_info])
# cursor.executemany('INSERT INTO reviews_info (info) VALUES (?)', [(info,) for info in reviews_info])

# # Commit and close
# conn.commit()
# conn.close()

# print("Data scraping and storage complete.")
