#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib import request

if __name__ == '__main__':
    # -----------向web服务器发送一个不完整的request--------
    # 设置url
    url = 'https://movie.douban.com/'
    # 获得网页回来的响应
    response1 = request.urlopen(url)
    # 读出响应体(此时得到字节码)，并进行转换为字符码
    my_html1 = response1.read().decode('utf-8')
    # print(my_html1)

    # -----------构建一个完整请求---------------------------
    # 设定请求头
    my_header = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64; x64)'
                        'AppleWebKit / 537.36(KHTML, like Gecko) '
                        'Chrome / 74.0.3729.108'
                        'Safari / 537.36'
    }
    # 用设定好的请求头创建一个完整请求
    my_request = request.Request(url=url, headers=my_header)
    # 用完整请求来获取响应
    my_response2 = request.urlopen(my_request)
    my_html2 = my_response2.read().decode('utf-8')
    print(my_html2)
