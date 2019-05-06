#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import request

if __name__ == '__main__':
    my_header = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64; x64)'
                        'AppleWebKit / 537.36(KHTML, like Gecko) '
                        'Chrome / 74.0.3729.108'
                        'Safari / 537.36'
    }
    url = 'https://jobs.51job.com/chengdu-whq/112433817.html?s=01&t=0'
    url2 = 'https://jobs.51job.com/chengdu-gxq/108054085.html?s=01&t=0'
    my_request = request.Request(headers=my_header, url=url2)
    my_response = request.urlopen(my_request, timeout=5)
    soup = BeautifulSoup(my_response.read(), 'html.parser')
    # print(soup.prettify())
    for i in soup.find_all(class_='bmsg job_msg inbox')[0].children:
        if i.name == 'p' or 'div':
            if i.string and i.string != '\n':
                print(i.string)
