#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib import request
import re


def get_html(url):
    my_header = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64; x64)'
                        'AppleWebKit / 537.36(KHTML, like Gecko) '
                        'Chrome / 74.0.3729.108'
                        'Safari / 537.36'
    }
    my_request = request.Request(url=url, headers=my_header)
    # 用完整请求来获取响应
    my_response = request.urlopen(my_request)
    return my_response.read().decode('GBK')


def crawler():
    url = 'https://read.fmx.cn/files/article/html/5/5/4/5/7/3/54573/index.html'
    return get_html(url)


def get_sub_url(html):
    """
    :param html
    :return:
    """
    # 正则
    p = re.compile(r'<span><a href="(.*?)">(.*?)</a></span>')
    return p.findall(html)


def get_text(html):
    p = re.compile(r'&nbsp;&nbsp;&nbsp;&nbsp;(.*?)\t\t\t\t\t\t          </p>\r\n          ', flags=re.S)
    return p.findall(html)


def save_text(title, text1):
    f = open('小说\\' + title, 'w', encoding='utf-8')
    f.write(text1.replace('&nbsp;', '').replace('<br />', ''))
    f.close()


if __name__ == '__main__':
    sub_urls = get_sub_url(crawler())
    for sub_url in sub_urls:
        text_html = get_html(r'https://read.fmx.cn/files/article/html/5/5/4/5/7/3/54573/' + sub_url[0])
        text = get_text(text_html)
        save_text(sub_url[1] + '.txt', text[0])
        print(sub_url[1] + '  保存完毕')
