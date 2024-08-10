import requests
from bs4 import BeautifulSoup
import pandas as pd


def fetch_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = []
    links = []
    images = []
    prices = []
    descs = []

    # Get all the titles with h1
    title_tag = soup.find(["h1"])
    titles.append(title_tag.get_text(strip=True))
    # print(titles)
    # Get all links with a tag and href
    for tag in soup.find_all("a", href=True):
        links.append(tag['href'])
    # print(links)
    # # Get all images with img tag and src
    for tag in soup.find_all('img', src=True):
        images.append(tag['src'])

    # Get all prices
    for tag in soup.find_all('p', class_="price"):
        prices.append(tag.get_text(strip=True))

  
    return {
        "title": titles,
        "image": images,
        "price": prices,
        "link": links
    }


urls = {
    "Avand": "https://avandmobile.com/product/samsung-galaxy-a10s-32g/",
    "Ecell": "https://www.ecell.ir/product/apple-watch-45mm-greenlion-hd-glass/",
    "Isatis": r"http://mobileisatis.ir/product/%da%af%d9%88%d8%b4%db%8c-%d8%a7%d9%be%d9%84-%d9%85%d8%af%d9%84-apple-iphone-13-128gb/"
}


data = {}

for website, url in urls.items():
    data[website] = fetch_data(url)
# print(data)


# text file
text_file = "scrapped.txt"


df = pd.DataFrame(data)

rows = []

for website_name, attributes in data.items():
    titles = attributes.get("title", [])
    images = attributes.get("image", [])
    prices = attributes.get("price", [])
    links = attributes.get("link", [])

   # maximum length of lists
    max_length = max(len(website_name), len(titles),
                     len(images), len(prices), len(links))

    # loop through inner lists
    for i in range(max_length):
        row = {
            "Website": website_name,
            "Title": titles[i] if i < len(titles) else None,
            "Image": images[i] if i < len(images) else None,
            "Price": prices[i] if i < len(prices) else None,
            "Link": links[i] if i < len(links) else None
        }

        rows.append(row)
df = pd.DataFrame(rows)

# Save  DataFrame to a CSV file
df.to_csv('scrapped.csv', index=False)

print("Data has been successfully written to 'scrapped.csv'")


# Write the data to a text file in a readable format
with open(text_file, "w", encoding="utf-8") as file:
    for webpage, info_list in data.items():
        file.write(f"{webpage}:\n")
        for item in info_list:
            file.write(f"  - {info_list}\n")
            break  # to stop the loop
        file.write("\n")

print(f"Data has been written to {text_file}")
