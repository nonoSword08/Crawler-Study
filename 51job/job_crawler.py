#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request
from urllib import error
from socket import timeout
import re


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
    # 爬取公司名字
    company_name = re.search(r'target="_blank" title="(.*?)" class="catn">', html).group(1)
    # 爬取岗位名称
    job_name = re.search(r'<h1 title="(.*?)">', html).group(1)
    # 爬取薪资水平
    salary = re.findall(r'<strong>(.*?)</strong>', html)[1]
    # 岗位学历要求
    try:
        education = re.search(r'高中|专科|中专|大专|本科|硕士', html).group()
    except AttributeError:
        education = '无'
    # 爬取工作年限
    try:
        work_year = re.search(r'&nbsp;(.{1,5}年经验)&nbsp;', html).group(1)
    except AttributeError:
        work_year = '无'
    # 爬取具体要求
    job_need = re.search(r'<div class="bmsg job_msg inbox"> *(.*?)<div class="mt10">', html, flags=re.S).group(1)
    print(company_name)
    print(job_name)
    print(salary)
    print(education)
    print(work_year)
    print(job_need.replace('</p><p>', '\n').replace('<span>', '').replace('</span>', '').replace('<br>', ''))
    print()


if __name__ == '__main__':
    work_address = {'chengdu': '090200', 'shanghai': '020000', 'beijing': '010000', 'guangzhou': '030200', 'shenzhen': '040000', 'hangzhou': '080200'}
    for city_name in work_address.keys():
        all_city_job_urls = []
        for page_num in range(1, 100):
            sub_urls_per_age = get_sub_url(get_html(r'https://search.51job.com/list/' +
                                                    work_address.get(city_name) +
                                                    ',000000,0000,00,9,99,python,2,' + str(page_num) + '.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=4&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='))
            if sub_urls_per_age is None:
                continue
            if not sub_urls_per_age:
                break
            # print(sub_urls_per_age)
            all_city_job_urls += sub_urls_per_age
            # time.sleep(0.5)
        print(all_city_job_urls)
        for job_info_url in all_city_job_urls:
            if city_name not in job_info_url:
                continue
            job_info_html = get_html(job_info_url)
            if job_info_html is not None:
                get_job_info(job_info_html)
