from pprint import pprint
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
    descriptions = []
    tables = []

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

    # to get description
    page_description = {}  # a dict to store our description with key and value
    div_tag = soup.find("div", id="tab-description")
    # print(div_tag)
    if div_tag:
        h2_tags = div_tag.find_all("h2")
        for index, h2 in enumerate(h2_tags, start=1):
            key = f"h2_{index}"
            page_description[key] = h2.get_text()

        h3_tags = div_tag.find_all("h3")
        for index, h3 in enumerate(h3_tags, start=1):
            key = f"h3_{index}"
            page_description[key] = h3.get_text()
        img_tags = div_tag.find_all("img")
        for index, img in enumerate(img_tags, start=1):
            key = f"img_{index}"
            page_description[key] = img.get("src")
        descriptions = [(k, v) for k, v in page_description.items()]
        # print(descriptions)

    # to get tables
    page_table = {}
    table_tag = soup.find("table", class_="shop_attributes")
    if table_tag:
        tr_tag = table_tag.find_all("tr")
        # print(type(tr_tag)) #---> <class 'bs4.element.ResultSet'>
        for tr in tr_tag:
            th_tag = tr.find("th")
            td_tag = tr.find("td")
            if td_tag and td_tag:
                key = th_tag.get_text(strip=True)
                value = td_tag.get_text(strip=True)
                page_table[key] = value
    tables = [(k, v) for k, v in page_table.items()]
    # pprint(tables)

    return {
        "title": titles,
        "image": images,
        "price": prices,
        "link": links,
        "description": descriptions,
        "table": tables
    }


urls = {
    "Avand": "https://avandmobile.com/product/samsung-galaxy-a10s-32g/",
    "Ecell": "https://www.ecell.ir/product/apple-watch-45mm-greenlion-hd-glass/",
    "Isatis": r"http://mobileisatis.ir/product/%da%af%d9%88%d8%b4%db%8c-%d8%a7%d9%be%d9%84-%d9%85%d8%af%d9%84-apple-iphone-13-128gb/"
}


data = {}

for website, url in urls.items():

    data[website] = fetch_data(url)
pprint(data)


# text file
text_file = "scrapped.txt"


df = pd.DataFrame(data)

rows = []

for website_name, attributes in data.items():
    titles = attributes.get("title", [])
    images = attributes.get("image", [])
    prices = attributes.get("price", [])
    links = attributes.get("link", [])
    descriptions = attributes.get("description", [])
    tables = attributes.get("table", [])

   # maximum length of lists
    max_length = max(len(website_name), len(titles),
                     len(images), len(prices), len(links), len(descriptions), len(tables))

    # loop through inner lists
    for i in range(max_length):
        row = {
            "Website": website_name,
            "Title": titles[i] if i < len(titles) else None,
            "Image": images[i] if i < len(images) else None,
            "Price": prices[i] if i < len(prices) else None,
            "Link": links[i] if i < len(links) else None,
            "Description": descriptions[i] if i < len(descriptions) else None,
            "Table": tables[i] if i < len(tables) else None
        }

        rows.append(row)
df = pd.DataFrame(rows)

# Save  DataFrame to a CSV file
df.to_csv('scrapped.csv', index=False)

# print("Data has been successfully written to 'scrapped.csv'")


# Write the data to a text file in a readable format
with open(text_file, "w", encoding="utf-8") as file:
    for webpage, info_list in data.items():
        file.write(f"{webpage}:\n")
        for item in info_list:
            file.write(f"  - {info_list}\n")
            break  # to stop the loop
        file.write("\n")

# print(f"Data has been written to {text_file}")
