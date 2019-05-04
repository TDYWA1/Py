# encoding=utf-8
import re
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class Jdlypar(object):
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def end(self):
        self.driver.quit()


class Checkedtag(Jdlypar):
    def __init__(self):
        super().__init__('http://www.jder.net/')
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.listu_n = []

    def gethottag(self, divclass):
        div = self.soup.find('div', {'class': divclass})
        for taga in div.find_all('a'):
            dictu_n = {}
            dictu_n[taga.text] = taga.get('href')
            self.listu_n.append(dictu_n)

    def getinput(self):
        print("*******************************绅士*************************************")
        for i in range(len(self.listu_n)):
            print(str(i + 1) + ".", list(dict(self.listu_n[i]).keys())[0], list(dict(self.listu_n[i]).values())[0])
        print("*******************************END*************************************")
        select = input("Please Make Your Choose:")
        return list(dict(self.listu_n[int(select) - 1]).values())[0]


class Picjdly(Jdlypar):
    def __init__(self, url):
        self.url = url
        super().__init__(url)
        self.refer = []
        self.pathname = []

    def allpage(self, pages, pagee):
        for page in range(int(pages), int(pagee) + 1):
            print("开始加载第%s页" % str(page))
            self.driver.get(self.url + 'page/%s/' % str(page))
            print("开始读取页面")
            self.getpage()
            self.getpic()
            print("第%s页下载完成！" % str(page))

    def getpage(self):
        self.refer.clear()
        self.pathname.clear()
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # soup=soup.find_all('section')
        soup = soup.find('main', {'id': 'main'})
        soup = soup.find_all('a')
        for item in soup:
            if item.find('img') != None:
                # print(item.get('href'))
                print(item.find('img').get('alt'))
                ########################################
                self.refer.append(item.get('href'))
                dirname = re.sub(r'[\\:：/]', '.', item.find('img').get('alt'))
                self.pathname.append(dirname)

    def getpic(self):
        for i in range(0, len(self.refer)):
            if not os.path.exists(self.pathname[i]):
                try:
                    os.mkdir(self.pathname[i])
                except:
                    print("创建目录失败")
                    continue
                print(self.pathname[i], "创建成功!")
            for j in range(1, 3):
                try:
                    r = requests.get(self.refer[i] + '/' + str(j), timeout=10)
                except:
                    print("gepic requests请求错误")
                    # os.rmdir(self.pathname[i])
                    continue
                if not r.status_code == 200:
                    print(self.refer[i], "链接不存在")
                    break
                soup = BeautifulSoup(r.text, 'html.parser')
                for item in soup.find_all('div'):
                    if item.get('class') == ['single-content']:
                        for img in item.find_all('img'):
                            picurl = img.get('src')
                            # print(picurl)
                            if re.match(r'^http:', picurl) == None:
                                picurl = 'http:' + picurl
                                # print(picurl)
                                # print(img.get('src'))
                                # print(re.match(r'^http',img.get('src')))
                            self.savepath = './' + self.pathname[i] + '/' + picurl.split('/')[-1]
                            self.savepic(picurl, self.refer[i])

    def savepic(self, url, refer=""):
        kv = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        kv['Referer'] = refer
        try:
            pic = requests.get(url, timeout=10, headers=kv)
            if pic.status_code == 200:
                with open(self.savepath, 'wb') as f:
                    f.write(pic.content)
                    print(self.savepath, "图片保存成功！")
            else:
                pic = requests.get(url, timeout=10)
                if pic.status_code == 200:
                    with open(self.savepath, 'wb') as f:
                        f.write(pic.content)
                        print(self.savepath, "图片保存成功！")
                else:
                    print("图片不存在")
        except:
            print("savepic requests请求错误")


class Alltest(object):
    def __init__(self, mode):
        self.mode = mode

    def start(self, pages, pagee):
        obj = Checkedtag()
        if self.mode == 0:
            print("按类别获取")
            obj.gethottag('menu-%e8%8f%9c%e5%8d%952-container')
        else:
            print("按热门标签获取")
            obj.gethottag('tagcloud')
        obj.end()
        url = obj.getinput()
        obj2 = Picjdly(url)
        obj2.allpage(pages, pagee)


if __name__ == '__main__':
    a = Alltest(0)
    a.start(1, 4)
