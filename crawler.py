import requests
from bs4 import BeautifulSoup
import sqlite3

url = "https://avandmobile.com/product/samsung-galaxy-a10s-32g/"

response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")



titles = soup.find_all("h1")
for title in titles:
    print(title.get_text())
    
links = soup.find_all("a")
for link in links:
    print(link.get("href"))

# prices = soup.find_all("div", {"class" : "price"})
# print(prices)

images = soup.find_all("img")
for image in images:
    print(image.get("src"))
    

feature_tabs = soup.find_all("ul", {"class" :"tabs"})

for feature_tab in feature_tabs:
    if feature_tab : soup.find_all("li", {"class" :"reviews_tab active"})
