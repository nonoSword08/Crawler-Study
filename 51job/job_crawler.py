#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request
from urllib import error
from socket import timeout
import re
import tkinter as tk
from openpyxl import Workbook
from openpyxl import load_workbook
from bs4 import BeautifulSoup


def get_html(url):
    my_header = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64; x64)'
                        'AppleWebKit / 537.36(KHTML, like Gecko) '
                        'Chrome / 74.0.3729.108'
                        'Safari / 537.36'
    }
    my_request = request.Request(url=url, headers=my_header)
    try:
        my_response = request.urlopen(my_request, timeout=10)
        html_content = my_response.read().decode('GBK')
    except (error.URLError, timeout, AttributeError):
        print('爬取失败')
        return None
    return html_content


def get_sub_url(html):
    try:
        p = re.compile(r'href="(.*?)" onmousedown="">')
    except TypeError:
        return None
    return p.findall(html)


def get_job_info(html):
    job_info_list = []
    # 爬取公司名字
    company_name = re.search(r'target="_blank" title="(.*?)" class="catn">', html).group(1)
    # 爬取岗位名称
    job_name = re.search(r'<h1 title="(.*?)">', html).group(1)
    # 爬取薪资水平
    salary = re.findall(r'<strong>(.*?)</strong>', html)[1]
    # 岗位学历要求
    try:
        education = re.search(r'初中|高中|专科|中专|大专|本科|硕士|博士|不限', html).group()
    except AttributeError:
        education = '无'
    # 爬取工作年限
    try:
        work_year = re.search(r'&nbsp;(.{1,5}年经验)&nbsp;', html).group(1)
    except AttributeError:
        work_year = '无'
    # 爬取具体要求
    soup = BeautifulSoup(html, 'html.parser')
    list1 = []
    for i in soup.find_all(class_='bmsg job_msg inbox')[0].children:
        if i.name == 'p' or 'div':
            if i.string and i.string != '\n':
                list1.append(i.string)
    job_need = '\n'.join(list1)
    print(job_need)
    job_info_list.append(company_name)
    job_info_list.append(job_name)
    job_info_list.append(salary)
    job_info_list.append(education)
    job_info_list.append(work_year)
    job_info_list.append(job_need)
    return job_info_list


def main():
    # 创建初始excle文件
    wb = Workbook()
    sheet = wb.active
    sheet.append(['公司名称', '职位名称', '薪资', '文化程度', '工作经验', '职位要求'])
    number = 0
    work_address = {'chengdu': '090200', 'shanghai': '020000', 'beijing': '010000', 'guangzhou': '030200',
                    'shenzhen': '040000', 'hangzhou': '080200'}
    for city_name in work_address.keys():
        for page_num in range(1, 100):
            sub_urls_per_age = get_sub_url(get_html(r'https://search.51job.com/list/' +
                                                    work_address.get(city_name) +
                                                    ',000000,0000,00,9,99,python,2,' +
                                                    str(page_num) +
                                                    '.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=4&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='))
            if sub_urls_per_age is None:
                continue
            if not sub_urls_per_age:
                break
            for job_info_url in sub_urls_per_age:
                if city_name not in job_info_url:
                    continue
                job_info_html = get_html(job_info_url)
                if job_info_html is not None:
                    sheet.append(get_job_info(job_info_html))
                    number += 1
                    if number == 300:
                        wb.save("job.xlsx")
                        return None


class Tker(object):
    def __init__(self):
        # 初始化主窗口
        self.root = tk.Tk()
        self.root.title('51job Crawler')
        # 新建Button
        self.button = tk.Button(self.root, text='开始爬取', command=main)
        # 布局
        self.button.pack()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    tk = Tker()
    tk.run()
