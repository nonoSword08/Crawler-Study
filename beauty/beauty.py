#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib import request
from urllib import error
from bs4 import BeautifulSoup

from time import sleep
import os


def get_soup(url):
    my_header = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64; x64)'
                        'AppleWebKit / 537.36(KHTML, like Gecko) '
                        'Chrome / 74.0.3729.108'
                        'Safari / 537.36'
    }
    my_request = request.Request(url=url, headers=my_header)
    my_response = request.urlopen(my_request, timeout=5).read().decode('GBK')
    soup = BeautifulSoup(my_response, 'html.parser')
    return soup


def get_people_pages(soup):
    people_pages = []
    for people in soup.find('div', {'class': 'MeinvTuPianBox'}).find_all(class_='tit'):
        people_pages.append([people['href'], people['title']])
    return people_pages


def get_img_info(url, title):
    soup = get_soup(url)
    return soup.find('img', {'alt': title})['src']


def save_img(url, path):
    img = request.urlopen(url, timeout=5).read()
    with open(path, 'wb') as f:
        f.write(img)


if __name__ == '__main__':
    for i in range(1, 2):
        url = 'https://www.2717.com/ent/meinvtupian/list_11_' + str(i) + '.html'
        people_pages = get_people_pages(get_soup(url))
        for people_page in people_pages:
            img_url = get_img_info('https://www.2717.com' + people_page[0], people_page[1])
            if img_url is None:
                continue
            dir_name = r'pic/' + people_page[1]
            os.mkdir(dir_name)
            if '-' not in img_url:
                img_url_head = img_url[:-5]
                for i in range(1, 100):
                    print(''.join([img_url_head, str(i), '.jpg']))
                    try:
                        save_img(''.join([img_url_head, str(i), '.jpg']), ''.join(['./pic/', people_page[1], '/', str(i), '.jpg']))
                        sleep(1)
                    except error.HTTPError:
                        print('该美女已经爬完')
                        break

