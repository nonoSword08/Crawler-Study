#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup
from win32com import client
import os


def get_soup(url):
    my_header = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64; x64)'
                        'AppleWebKit / 537.36(KHTML, like Gecko) '
                        'Chrome / 74.0.3729.108'
                        'Safari / 537.36'
    }
    my_request = request.Request(url=url, headers=my_header)
    my_response = request.urlopen(my_request, timeout=5)
    soup = BeautifulSoup(my_response, 'html.parser')
    return soup


if __name__ == '__main__':
    # 保存html
    soup = get_soup('https://blog.csdn.net/CSDNedu/article/details/89917111')
    article = soup.find('article')
    with open('temp.html', 'w+', encoding='utf-8') as f:
        f.write('<!Doctype html>\n')
        f.write(article.prettify())
    # 将html转化为word
    path = os.getcwd() + r'/temp'
    word = client.Dispatch('Word.Application')
    doc = word.Documents.Open(path + '.html')
    doc.SaveAs(path + '.doc', FileFormat=0)
    doc.Close(-1)
    os.remove(path + '.html')
