parent_div = soup.find("div", class_="elementor-widget-container")
for tag in parent_div:
    p_tag = tag.find_all("p")
    for tag in p_tag:
        print(p_tag.get_text(strip=True))