from bs4 import BeautifulSoup

html = '''<td class="title black">
    <div class="tit3" id="my-div">
        <a href="/movie/bi/mi/basic.nhn?code=161967" title="기생충">기생충</a>
    </div>
</td>'''


# 1. tag 조회
def ex1():
    bs = BeautifulSoup(html, 'html.parser')
    # print(bs)
    # print(type(bs))

    tag = bs.td
    # print(tag)
    # print(type(tag))

    # tag = bs.div
    # print(tag)
    # print(type(tag))

    tag = bs.a
    # print(tag)
    # print(type(tag))

    tag = bs.td.div
    # print(tag)
    # print(type(tag))


# 2. attribute 조회
def ex2():
    bs = BeautifulSoup(html, 'html.parser')
    tag = bs.td

    print(tag['class'])

    tag = bs.div
    # print(tag['id'])      없는 값은 Error!
    print(tag.attrs)


# 3. attribute로 태그 조회
def ex3():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.find('td', attrs={'class': 'title'})
    print(tag)

    tag = bs.find(attrs={'class'})


if __name__ == '__main__':
    ex1()
    ex2()
