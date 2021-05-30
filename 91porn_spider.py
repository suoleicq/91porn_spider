import os
import re
import multiprocessing as np
import urllib.request
import requests
import time
from progressbar import *
from multiprocessing.dummy import Pool as ThreadPool
import shutil
import sys

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Content-Type': 
        'text/html; charset=UTF-8',
    'Cookie':
        '__utmz=50351329.1619103318.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cf_clearance=fe1ff244a0c09d9c94751debbf235924654ba65d-1622268711-0-150; __utmc=50351329; CLIPSHARE=dsk6btimjontv94uivjobd7q9g; __utma=50351329.1539335310.1619103318.1622270967.1622288651.6; __utmb=50351329.0.10.1622288651'
}
proxies = {}

class spider():
    def __init__(self, parent=None):
        self.items_all = []
        self.mv_flag = ""


    def run(self):
        mv = input("请选择爬取类型: 1-今日最热  2-本月最热  3-最近加精  4=本月收藏  5-本月讨论 6-上月最热\r\n") 
        pages = input("请输入要爬取的页数:")
        self.list_page(self.get_button(mv),pages)
        self.dl_main()

    def get_button(self,button):
        
        if "1" in button:
            url='http://91porn.com/v.php?category=hot&viewtype=basic&page='
            self.mv_flag = "当前最热"
        elif "2" in button:
            url='http://91porn.com/v.php?category=top&viewtype=basic&page='
            self.mv_flag = "本月最热"
        elif "3" in button:
            url='http://91porn.com/v.php?category=rf&viewtype=basic&page='
            self.mv_flag = "最近加精"
        elif "4" in button:
            url='http://91porn.com/v.php?category=tf&viewtype=basic&page='
            self.mv_flag = "本月收藏"
        elif "5" in button:
            url='http://91porn.com/v.php?category=md&viewtype=basic&page='
            self.mv_flag = "本月讨论"
        elif "6" in button:
            url='http://91porn.com/v.php?category=top&m=-1&viewtype=basic&page='
            self.mv_flag = "上月最热"
        return url

    def list_page(self,url,pages):
        o_url = url
        for i in range(1,int(pages)+1):
            url = o_url+str(i)
            res = requests.get(url,headers=headers)
            if res.status_code==200:
                print(url)
                main_page = res.text
                pattern = re.compile('.*?<img class="img-responsive" src="https://i.p04.space/thumb/(.*?).jpg.*?<span class="video-title title-truncate m-t-5">(.*?)</span>.*?',re.S)
                items = re.findall(pattern,main_page)
                self.items_all.append(items)
                pool = ThreadPool(10) #双核电脑
                pool.map(self.show,items)#多线程工作
                pool.close()
                pool.join()
            else:
                print("请求网页失败，请检查网页URL是否正确------------\r\n")
        print("==================已全部获取完成，开始下载！\r\n")
    def show(self,items):
        title = items[1]
        print("===============已获取："+str(title)+".mp4\r\n")
    def dl_main(self):
        if not os.path.exists("91porn/"+self.mv_flag):
            os.makedirs("91porn/"+self.mv_flag)
        for item in self.items_all:
            pool = ThreadPool(10) #双核电脑
            pool.map(self.download, item)#多线程工作
            pool.close()
            pool.join()
    def download(self,items):
        time.sleep(2)
        id = items[0]
        title = items[1]
        base_dir="https://cdn.91p07.com//m3u8//"
        fragment=0
        
        save_path = "91porn//"+self.mv_flag+"//"+title
        hbpath = save_path+ ".mp4"
        if os.path.exists(hbpath):
            print("============="+hbpath+"：已存在，将跳过该视频\r\n")
        else:
            while True:
                url = base_dir+id+"//"+id+str(fragment)+".ts"
                r = requests.get(url) 
                if r.ok==True:
                    with open(hbpath,'ab') as f:
                        f.write(r.content)
                    fragment=fragment+1
                else:
                    print("==================下载完成："+hbpath +"\r\n")
                    break
if __name__ == '__main__':
    s = spider()
    s.run()
    
