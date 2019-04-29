# encoding=utf-8
'''
替换指定字符串，可通过正则表达式匹配
pattern指定表达式
'''

import os
import re
pattern='F.+'
def sech(texta):
    f=open('10.txt')
    strf=f.read()
    f.close()
    print(strf)
    ls=re.sub(texta,'F100',strf)
    print(ls)
    f1=open('6.txt','w')
    f1.write(ls)
    f1.close()


sech(pattern)