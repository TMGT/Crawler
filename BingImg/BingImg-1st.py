# get img url from index source code
# coding=utf-8

import requests
import re
import time


def get_html_text(url):
    req = requests.get(url)
    req.raise_for_status()
    req.encoding = req.apparent_encoding
    return req.text


def get_img_link(html):
    pat = re.compile("url\: \".+?\"")
    result = pat.findall(html)[0].split('"')[1]
    url = "https://www.bing.com" + result
    return url


def download_img(url):
    req = requests.get(url)
    date = time.strftime("%Y-%m-%d")
    file_path = "I:\\BingImg\\" + date + ".jpg"  # set path here
    with open(file_path, "wb") as f:
        f.write(req.content)


if __name__ == "__main__":
    html_text = get_html_text("https://www.bing.com/?intlF=")
    img_link = get_img_link(html_text)
    download_img(img_link)
