import json
import jsonlines
import os
import requests
import wget
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

work_dir = os.getcwd()

def mkdir(path):

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\/")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.mkdir(path)



def api_download(url, dir):
    # 使用无头模式打开chrome
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:7891")
    # dir = '/home/tustxsfh/音乐/spotlight'
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory':dir}
    chrome_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.implicitly_wait(60 * 3)
    browser.maximize_window()
    browser.get(url)
    time.sleep(10)



with open('result.json', 'r+') as f:
  
    for item in jsonlines.Reader(f):

        cate_name = item['category_name']

        print('进入'+cate_name+'分类')

        article_title = item['article_title']
        article_pic = item['article_pic']
        text = item['text']
        api = item['mp3_download_api']
        youtube_url = item['youtube_url']


        path = os.path.join(work_dir, cate_name)
        mkdir(path)
        os.chdir(path)

        path = os.path.join(path, article_title)
        mkdir(path)
        os.chdir(path)

        if article_pic:
            wget.download(article_pic)
            print(article_title+'图片下载完毕')

        if text:
            with open('article.txt', 'w') as f:
                f.write(text)
            print(article_title+'文字下载完毕')    

        if api:
            dir = os.getcwd()
            api_download(api, dir)
            print(article_title+'音频下载完毕')
        
        
        # if youtube_url:
        #     os.system('youtube-dl -i --proxy socks5://127.0.0.1:7891/ youtube_url')
        #     print(article_title+'视频下载完毕')

        time.sleep(10)







