#-*- coding: utf-8 -*-
import requests
import bs4

import subprocess
import json

import os


# Requests
TARGET_URL = "http://search.daum.net/search?q=%EB%A9%A4%EB%B2%84%EB%B6%81&w=news&cluster_docid=26MyjuL0jT59us99pD"
data = requests.get(TARGET_URL)

# Parsing ( BeautifulSoup4 )
data = bs4.BeautifulSoup(data.text)
articles = data.findAll("div", attrs={'class': 'cont_inner'})

article_data = []
for article in articles:
    title_and_link = article.findAll("a")[0]
    title = title_and_link.text.encode('utf-8')
    link = title_and_link["href"]

    date_and_media = str(article.findAll("span", attrs={'class': 'date'})[0])
    date = date_and_media.split("\n")[1]
    media = date_and_media.split("\n")[2].split("</span> ")[1]

    article_data.append(
        {
            "title": title,
            "link": link,
            "date": date,
            "media": media,
        }
    )

    # ScreenShot
    subprocess.call([
        "webkit2png",
        "-F",   # only create fullsize screenshot
        "--filename=temp",
        "--dir=images",
        link
    ])


    # Rename Screenshot
    # webkit2png --filename=FILENAME 옵션을 사용하면 한글깨짐 문제 발생
    for filename in os.listdir("./images/"):
        if filename.startswith("temp"):
            os.rename(
                os.path.join(os.getcwd(), "images", filename),
                os.path.join(os.getcwd(), "images",
                             "Screenshot_" + date + "_" + media + "_" + title.replace(" ", "_") + ".png")
            )

# Result as JSON
# 단, ensure_ascii 옵션으로 UTF-8 ( 한글로 보이도록 ) 출력한다.
with open('result.json', 'w') as outfile:
    json.dump(article_data, outfile, ensure_ascii=False)
