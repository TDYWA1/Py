# coding=utf-8

CLASSOFALL = {
    '欧美': 'https://music.163.com/#/discover/playlist/?cat=%E6%AC%A7%E7%BE%8E',
    '日语': 'https://music.163.com/#/discover/playlist/?cat=%E6%97%A5%E8%AF%AD',
    '粤语': 'https://music.163.com/#/discover/playlist/?cat=%E7%B2%A4%E8%AF%AD',
    '流行': 'https://music.163.com/#/discover/playlist/?cat=%E6%B5%81%E8%A1%8C',
    '民谣': 'https://music.163.com/#/discover/playlist/?cat=%E6%B0%91%E8%B0%A3',
    '电子': 'https://music.163.com/#/discover/playlist/?cat=%E7%94%B5%E5%AD%90',
    '乡村': 'https://music.163.com/#/discover/playlist/?cat=%E4%B9%A1%E6%9D%91',
    '古典': 'https://music.163.com/#/discover/playlist/?cat=%E5%8F%A4%E5%85%B8',
    '古风': 'https://music.163.com/#/discover/playlist/?cat=%E5%8F%A4%E9%A3%8E',
    '清晨': 'https://music.163.com/#/discover/playlist/?cat=%E6%B8%85%E6%99%A8',
    '夜晚': 'https://music.163.com/#/discover/playlist/?cat=%E5%A4%9C%E6%99%9A',
    '下午茶': 'https://music.163.com/#/discover/playlist/?cat=%E4%B8%8B%E5%8D%88%E8%8C%B6',
    '散步': 'https://music.163.com/#/discover/playlist/?cat=%E6%95%A3%E6%AD%A5',

}
logurl = 'https://music.163.com/login'

import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from selenium import webdriver
import time

lis1 = []
lis2 = []
mes = {}
URL = []
url = ''

option = webdriver.ChromeOptions()
option.add_argument('--no-sandbox')
option.add_argument('--headless')
# 注意path
web = webdriver.Chrome(options=option)


def selectitem():
    d = {}
    print("请选择项目")
    j = 0
    for item in CLASSOFALL:
        j += 1
        print(str(j) + ':' + item)
        d[str(j)] = item
    strr = input("请输入你的选择（多项可直接输入，以空格分割）")
    urll = re.findall('(\d{1,2}) ', strr)
    for i in urll:
        URL.append(CLASSOFALL[d[i]])
    CLASSOFALL.clear()


# 账号密码登录
def login163byap():
    web.get(logurl)
    web.switch_to.frame('contentFrame')
    tagsa = web.find_elements_by_tag_name('a')
    for taga in tagsa:
        print(taga.text)
        if taga.text == '手机号登录':
            print("")
            taga.click()
            web.switch_to.default_content()
            time.sleep(1)
            ipt = web.find_elements_by_tag_name('input')
            for ip in ipt:
                if ip.size == {'height': 30, 'width': 222}:
                    ip.click()
                    ip.send_keys("15857732394")
                if ip.size == {'height': 32, 'width': 220}:
                    ip.click()
                    ip.send_keys("zmx19981314")

            tagsa = web.find_elements_by_tag_name('a')
            for tagaa in tagsa:
                if tagaa.text == "登　录":
                    tagaa.click()
                    time.sleep(1)
                    break
        break

    print("登录成功！")
    # os.system('pause')


# 初始化 返回浏览器handle
def init():
    login163byap()


# 读取网页返回歌单列表/链接地址/播放量
def duqu(webt):
    soup = BeautifulSoup(webt, 'html.parser')
    soup.prettify()
    la = soup.find_all('a')
    sp = soup.find_all('span')

    for i in range(len(la)):
        if la[i].get('class') == ['msk']:
            st = "歌单名：" + la[i].get('title') + " 地址：" + "https://music.163.com/#" + la[i].get('href')
            print(st)
            lis1.append(st)

    for i in range(len(sp)):
        if sp[i].get('class') == ['nb']:
            lis2.append(sp[i].string)


# 对歌单按播放量排序
def sortli():
    d = {}
    for i in range(len(lis1)):
        print(lis1[i])
        print(lis2[i])
        lis2[i] = re.sub(r'万', '0000', lis2[i])
        print(lis2[i])
        if int(lis2[i]) >= 1000000:
            d[lis1[i]] = int(lis2[i])
    dv = sorted(d.values(), reverse=True)
    di = d
    for j in dv:
        for i in di.keys():
            if di[i] == j:
                res = re.search(r'https:.*', i)
                # print(res.group()+" 播放量："+str(j))
                d[res.group()] = str(j)
                del di[i]
                break
    lis1.clear()
    lis2.clear()
    return d


# 对指定歌单的歌曲加入mes字典
def prmusic():
    mes1 = []
    mes2 = []
    mes3 = []
    soup = BeautifulSoup(web.page_source, "html.parser")
    tags = soup.find_all('span')
    for tag in tags:
        if tag.get('class') == ['txt']:
            tagsa = tag.find_all('a')
            for taga in tagsa:
                mes1.append("https://music.163.com/#" + taga.get('href'))
            tagsa = tag.find_all('b')
            for taga in tagsa:
                mes2.append(taga.get('title'))
    tags = soup.find_all('div')
    for tag in tags:
        if tag.get('class') == ['text']:
            if tag.get('title') != None:
                mes3.append(tag.get('title'))
    for i in range(len(mes1)):
        if not mes1[i] in mes.keys():
            mes[mes1[i]] = mes2[i] + " " + mes3[i] + " " + str(1)
        else:
            stra = mes[mes1[i]].split(" ")
            stra[-1] = str(int(stra[-1]) + 1)
            strb = stra[0]
            for item in range(1, len(stra)):
                strb += " " + stra[item]
            mes[mes1[i]] = strb
    print("共", len(mes), "首")
    return mes


# 对所有指定歌单执行prmusic()操作
def huoqugm(zid):
    for item in zid:
        print(item, zid[item])
        web.get(item)
        web.switch_to.frame('contentFrame')
        time.sleep(1)
        prmusic()
        # break


# 加入歌单操作
def addtolist(addr, nameli):
    web.get(addr)
    web.switch_to.frame('contentFrame')
    tagsa = web.find_elements_by_tag_name('i')
    for taga in tagsa:
        if taga.text == "收藏":
            taga.click()
            break
    time.sleep(2)
    tagsa = web.find_elements_by_tag_name('p')
    for taga in tagsa:
        if taga.text == nameli:
            taga.click()
            time.sleep(0.5)
            print(mes[addr] + "保存成功！")
            break


def addtoall():
    number1 = 0
    number2 = 0
    number3 = 0
    for item in mes:
        if pickup(item, 9):
            addtolist(item, "AJ20")
            number1 += 1
        elif pickup(item, 6):
            addtolist(item, "AJ10")
            number2 += 1
        elif pickup(item, 3):
            addtolist(item, "AJ05")
            number3 += 1
        del item
    mes.clear()
    print(str(number1), "首")
    print(str(number2), "首")
    print(str(number3), "首")
    print("共", str(number1 + number2 + number3), "首")


# 筛选函数
def pickup(link, numbi):
    num = mes[link].split(" ")
    i = int(num[-1])
    if i > numbi:
        return True


# 显示mes字典
def prt():
    for item in mes:
        print(item, mes[item] + "次", sep="  ")


def page1():
    web.get(url)
    time.sleep(2)
    web.switch_to.frame('contentFrame')
    duqu(web.page_source)
    zid = sortli()
    print(zid)
    huoqugm(zid)
    prt()
    print("开始保存")
    addtoall()


# 读取所有页码/配合duqu()
def readpage(i):
    print("读取第{}页".format(str(i)))
    web.get(url + "&limit=35&offset=" + str((i - 1) * 35))
    web.switch_to.frame('contentFrame')
    time.sleep(1)
    duqu(web.page_source)


def pageall():
    for i in range(PageStart, PageEnd):
        readpage(i)
        zid = sortli()
        print(zid)
        huoqugm(zid)
        prt()
        print("开始保存")
        addtoall()


PageStart = 2
PageEnd = 30

selectitem()
print(URL)
init()
for f in range(0, len(URL)):
    url = URL[f]
    page1()
    pageall()
    lis1.clear()
    lis2.clear()
    mes.clear()
