#! /usr/bin/env python3

'''
从firefox中尝试点击不同页面,发现访问的URL分别为
https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?from_mid=1&format=json&ie=utf-8&oe=utf-8&subtitle=%E6%A0%BC%E8%A8%80&query=%E6%A0%BC%E8%A8%80&rn=8&pn=0&resource_id=6844&cb=jQuery110208193217330929087_1488263284684&_=1488263284688

https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?from_mid=1&format=json&ie=utf-8&oe=utf-8&subtitle=%E6%A0%BC%E8%A8%80&query=%E6%A0%BC%E8%A8%80&rn=8&pn=8&resource_id=6844&cb=jQuery110208193217330929087_1488263284684&_=1488263284686

https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?from_mid=1&format=json&ie=utf-8&oe=utf-8&subtitle=%E6%A0%BC%E8%A8%80&query=%E6%A0%BC%E8%A8%80&rn=8&pn=16&resource_id=6844&cb=jQuery110208193217330929087_1488263284684&_=1488263284687
'''
import json
import sys
import requests

def request_proverb(start,number):
    '''从百度那获取格言信息,START为起始条数,NUMBER为获取格言条数,不能超过50'''
    url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php"
    params = {"from_mid":1,
              "format":"json",
              "ie":"utf-8",
              "oe":"utf-8",
              "subtitle":"格言",
              "query":"格言",
              "rn":number,
              "pn":start,
              "resource_id" : 6844}
    response = requests.get(url,params=params)
    response = json.loads(response.text)
    status = response.get('status')
    if status != "0":
        raise Exception()
    data = response.get('data')[0]
    resNum = data.get('resNum')
    proverbs = data.get('disp_data')
    return proverbs

def proverb_to_fortune_item(proverb):
    author = proverb.get('author')
    ename = proverb.get('ename')
    return "{ename}\n\t-{author}\n%\n".format(ename=ename,author=author)

def proverbs_to_fortune_file(proverbs,fortune_file):
    with open(fortune_file,mode="a") as f:
        for proverb in proverbs:
            item = proverb_to_fortune_item(proverb)
            f.write(item)

if  __name__ == "__main__":
    fortune_file = sys.argv[1]
    start = 0
    number =10
    while True:
        proverbs = request_proverb(start,number)
        if not proverbs:
            break
        proverbs_to_fortune_file(proverbs,fortune_file)
        start+=number
