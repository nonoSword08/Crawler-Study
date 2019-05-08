#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib import request
from urllib import error
from bs4 import BeautifulSoup

import os


def get_soup(url):
    my_header = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64; x64)'
                        'AppleWebKit / 537.36(KHTML, like Gecko) '
                        'Chrome / 74.0.3729.108'
                        'Safari / 537.36'
    }
    my_request = request.Request(url=url, headers=my_header)
    my_response = request.urlopen(my_request, timeout=10).read().decode('GBK')
    soup = BeautifulSoup(my_response, 'html.parser')
    return soup


def get_people_pages(soup):
    people_pages = []
    for people in soup.find('div', {'class': 'MeinvTuPianBox'}).find_all(class_='tit'):
        people_pages.append([people['href'], people['title']])
    return people_pages


def get_img_url(url, title):
    soup = get_soup(url)
    return soup.find('img', {'alt': title})['src']


def save_img(url, path):
    img = request.urlopen(url, timeout=10).read()
    with open(path, 'wb') as f:
        f.write(img)


if __name__ == '__main__':
    try:
        os.mkdir('./pic')
    except FileExistsError:
        pass
    # 一共有221页
    for page_num in range(1, 222):
        url = 'https://www.2717.com/ent/meinvtupian/list_11_' + str(page_num) + '.html'
        try:
            people_pages = get_people_pages(get_soup(url))
        except BaseException:
            print('获取%d种子url失败' % page_num)
            people_pages = None
        print('正在爬取第%d页'.center(200, '*'))
        if people_pages is None:
            continue
        for people_page in people_pages:
            # 创建子目录
            dir_name = ''.join(list(filter(lambda x: x not in r'0123456789()', r'pic/' + people_page[1])))
            try:
                os.makedirs(dir_name)
            except FileExistsError:
                pass
            # 爬取每张图片
            for img_num in range(1, 1000):
                try:
                    img_url = get_img_url(''.join(['https://www.2717.com', people_page[0][:-5], '_', str(img_num), '.html']),
                                          people_page[1]
                                          )
                    img_path = ''.join([dir_name, '/', str(img_num), '.jpg'])
                    # print(img_url, img_path)
                    save_img(img_url, img_path)
                except error.HTTPError:
                    print('爬取 %s 完成' % people_page[1])
                    break
                except BaseException:
                    print('爬取 %s 第%d张图片失败  地址  %s  ' % (people_page[1], img_num, ''.join(['https://www.2717.com', people_page[0][:-5], '_', str(img_num), '.html'])))
                    continue

