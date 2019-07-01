import ssl
import sys
import time
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler


def crawling_pelicana():
    results = []
    for page in count(start=1):

        url = 'https://pelicana.co.kr/store/stroe_search.html?gu=&si=&page=%d' % page

        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]
            results.append((name, address) + tuple(sidogu))

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/pelicana.csv', encoding="utf-8", mode='w', index=True)


def crawling_nene():
    results = []
    firstname = ''
    currentname = ' '
    for page in range(1, 5):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?page=%d&ex_select=1&ex_select2=&IndexSword=&GUBUN=A' % page

        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        divs = bs.find('div', attrs={'class': 'shopWrap'})
        shoplist = divs.findAll('div', attrs={'class': 'shop'})
        currentname = shoplist[0].find('div', attrs={'class': 'shopName'}).text
        if firstname == currentname:
            break
        firstname = currentname

        for shop in shoplist:

            strings = list(shop.strings)

            if strings[8] == 'Pizza':
                name = strings[12]
                address = strings[14]
                sidogu = address.split()[:2]
            else:
                name = strings[10]
                address = strings[12]
                sidogu = address.split()[:2]
            results.append((name, address) + tuple(sidogu))

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/nene.csv', encoding="utf-8", mode='w', index=True)


def crawling_kyochon():
    results = []
    for sido in range(1,18):
        for sido2 in range(1,27):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch='%(sido, sido2)
            html = crawler.crawling(url)

            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_spans = bs.findAll(attrs={'class': 'store_item'})

            for tag_span in tag_spans:
                strings = list(tag_span.strings)
                name = strings[1]
                # 공백 및 개행 제거
                addr = strings[3].strip('\r\n\t')
                sidogu = addr.split()[:2]

                results.append((name, addr) + tuple(sidogu))

    for t in results:
        print(t)

    # 저장
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/kyochon.csv', encoding='utf-8', mode='w', index=True)


def crawling_goobne():
    results = []
    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    # 첫 페이지 로딩
    wd = webdriver.Chrome('D:\cafe24\chrome_driver/chromedriver.exe')
    wd.get(url)
    time.sleep(3)

    for page in count(start=1):

        # 자바 스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now()}: success for request [{script}]')
        time.sleep(2)

        # 실행 결과 HTML(동적으로 렌더링 된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # detect last page
        if tags_tr[0].get('class') is None:
            wd.quit()
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)

            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]
            results.append((name, address)+tuple(sidogu))

    wd.quit()

    # 저장
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/goobne.csv', encoding='utf-8', mode='w', index=True)


if __name__ == '__main__':
    # crawling_pelicana()
    crawling_nene()
    # crawler.crawling()
    # crawling_kyochon()
    # crawling_goobne()

