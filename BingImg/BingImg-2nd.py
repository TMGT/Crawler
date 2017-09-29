# get img url from json file
# coding = utf-8

import requests
import json
import time


def get_json_text(url):
    req = requests.get(url)
    req.raise_for_status()
    req.encoding = req.apparent_encoding
    text = req.text
    return text


def get_img_url(html):
    json_file = json.loads(html)
    result = json_file["images"][0]["url"]
    url = "https://www.bing.com" + result
    return url


def download_img(url):
    req = requests.get(url)
    date = time.strftime("%Y-%m-%d")
    file_path = "I:\\BingImg\\" + date + ".bmp"
    with open(file_path, "wb") as f:
        f.write(req.content)


if __name__ == "__main__":
    url = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
    html = get_json_text(url)
    img_url = get_img_url(html)
    download_img(img_url)








































'''
'''
