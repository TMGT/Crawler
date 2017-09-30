# get img url from json file
# coding = utf-8

import requests
import json
import os
import time
import win32con
import win32gui


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


def get_path():
    abs_path = os.path.split(os.path.realpath(__file__))[0]
    current_path = abs_path + "\\"
    date = time.strftime("%Y-%m-%d")
    img_path = current_path + date + ".bmp"
    return img_path


def download_img(url, save_path):
    req = requests.get(url)
    with open(save_path, "wb") as f:
        f.write(req.content)


def set_wallpaper(img_path):
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_path, 1 + 2)
    time.sleep(3)
    os.remove(img_path)


if __name__ == "__main__":
    url = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
    html = get_json_text(url)
    img_url = get_img_url(html)
    path = get_path()
    download_img(img_url, path)
    set_wallpaper(path)








































'''
'''
