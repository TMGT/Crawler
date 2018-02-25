# coding: utf-8
# Py -V : 3.6
# author: TMGT
# time  : 2018/2/22 17:03

import requests
import re
import os
import time
from bs4 import BeautifulSoup


class V2EX:

    def __init__(self, user_name, user_password):

        self._user_name = user_name
        self._user_password = user_password
        self._session = requests.Session()
        self.islogin = False
        self._header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Origin": "https://www.v2ex.com",
            "Referer": "https://www.v2ex.com/signin",
            "Host": "www.v2ex.com"
        }

    def login(self):

        login_page = self._session.get("https://www.v2ex.com/signin", headers=self._header)
        data_key = re.findall('sl" name="\w+?"', login_page.text)
        name_key = data_key[0].split('"')[-2]
        password_key = data_key[1].split('"')[-2]
        verification_code_key = data_key[2].split('"')[-2]
        once = re.search('value="\d+"', login_page.text).group(0).split('"')[-2]
        verification_code_url = "https://www.v2ex.com/_captcha?once={}".format(once)

        with open(os.getcwd()+"\code.png", "wb") as f:
            f.write(self._session.get(verification_code_url, headers=self._header).content)

        verification_code = input("请输入验证码:\n")

        post_data = {
            name_key: self._user_name,
            password_key: self._user_password,
            verification_code_key: verification_code,
            "once": once,
            "next": "/"
        }

        self._session.post("https://www.v2ex.com/signin", data=post_data, headers=self._header)
        setting_page = self._session.get("https://www.v2ex.com/settings", headers=self._header)

        if re.search(self._user_name, setting_page.text).group(0):
            self.islogin = True
            return "login_success"
        else:
            return "login_failed"

    def sign(self):

        if self.islogin:
            pass
        else:
            return "您还未登录，请先登录"

        mission_page = self._session.get("https://www.v2ex.com/mission/daily", headers=self._header)
        url_pattern = re.compile("""onclick="location.href = '/\S+?'""")

        harf_url = url_pattern.search(mission_page.text).group(0).split("'")[-2]
        sign_url = "https://www.v2ex.com"+str(harf_url)

        header = self._header
        header["Referer"] = "https://www.v2ex.com/mission/daily"

        balance_url = "https://www.v2ex.com/balance"

        soup_1 = BeautifulSoup(self._session.get(balance_url, headers=header).text, "lxml")
        balance_1 = soup_1.select(".balance_area")[0].text

        self._session.get(sign_url, headers=header)

        soup_2 = BeautifulSoup(self._session.get(balance_url, headers=header).text, "lxml")
        balance_2 = soup_2.select(".balance_area")[0].text

        if balance_1 != balance_2:
            return "sign_success"
        else:
            return "sign_failed"


if __name__ == "__main__":

    user_name = input("请输入用户名:\n")
    user_password = input("请输入密码:\n")
    test = V2EX(user_name, user_password)
    print(test.login())
    time.sleep(2)
    print(test.sign())
    time.sleep(3)


