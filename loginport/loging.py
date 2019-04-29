# coding=utf8
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
"""
网站登录接口

"""

class Login:
    def __init__(self,driver,username,password):
        print("欢迎使用！")
        self.brower = driver
        self.username = username
        self.password = password
        self.url163music = "https://music.163.com/login"

    def login163music(self):
        self.brower.get(self.url163music)
        self.brower.switch_to.frame('contentFrame')
        tagsa = self.brower.find_elements_by_tag_name('a')
        for taga in tagsa:
            print(taga.text)
            if taga.text == '手机号登录':
                print("正在登录。。。")
                taga.click()
                self.brower.switch_to.default_content()
                time.sleep(1)
                ipt = self.brower.find_elements_by_tag_name('input')
                for ip in ipt:
                    if ip.size == {'height': 30, 'width': 222}:
                        ip.click()
                        ip.send_keys(self.username)
                    if ip.size == {'height': 32, 'width': 220}:
                        ip.click()
                        ip.send_keys(self.password)
                tagsa = self.brower.find_elements_by_tag_name('a')
                for tagaa in tagsa:
                    if tagaa.text == "登　录":
                        tagaa.click()
                        time.sleep(1)
                        break
            break
        print("登录成功！")
        print("谢谢使用！")
        return self.brower
        # os.system('pause')
