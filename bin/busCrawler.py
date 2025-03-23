import requests
from bs4 import BeautifulSoup

url = "https://www.fukuyama-u.ac.jp/campuslife/student-affairs/attending-school/"


def busCrawler():
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'html.parser')

    starting_element = soup.find(string="無料スクールバス運行アナウンス").find_parent('p')
    # print(f'起始坐标元素： {starting_element}')
    ending_element = soup.find(string="スクールバス時刻表").find_parent().find_parent().find_parent().find_parent()
    # print(f'结束坐标元素： {ending_element}')
    index_element = starting_element.find_next_sibling()

    buff_element = []

    while index_element != ending_element:
        buff_element.append(index_element)
        index_element = index_element.find_next_sibling()

    buff_element.pop()

    buff_titles = []
    buff_links = []

    isTitle = True

    for i in buff_element:
        if isTitle:
            buff_titles.append(i.get_text())
            isTitle = False
        else:
            buff_links.append(i.find('a')['href'])
            isTitle = True

    # print(f'找到{int(len(buff_element)/2)}张校车表')
    # for i in range(len(buff_titles)):
    #     print(f'标题：{buff_titles[i]}\n链接：{buff_links[i]}')
    return buff_titles, buff_links