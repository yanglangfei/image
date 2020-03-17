# coding:utf-8
import requests
import multiprocessing
from bs4 import BeautifulSoup
import re
import os
import time
import threading


def get_pages(url):
    soup = ""
    try:
        # 创建请求日志文件夹
        if 'Log' not in os.listdir('.'):
            os.mkdir(r".\Log")

        # 请求当前章节页面  params为请求参数
        response = requests.get(url)
        content = response.content
        data = content.decode('gbk')
        # soup转换
        soup = BeautifulSoup(data, "html.parser")

    except Exception as e:
        print(url + " 请求错误\n")
        with open(r".\Log\req_error.txt", 'a', encoding='utf-8') as f:
            f.write(url + " 请求错误\n")
        f.close()
    return soup


# 通过章节的url下载内容，并返回下一页的url
class get_ChartTxt(threading.Thread):
    def __init__(self, url, title, num):
        super(get_ChartTxt, self).__init__()
        self.url = url
        self.title = title
        self.num = num

    def run(self):
        try:
            soup = get_pages(self.url)
            # 获取章节名称
            subtitle = soup.select('#directs > div.bookInfo > h1 > strong')[0].text
            # 判断是否有感言
            if re.search(r'.*?章', subtitle) is None:
                return
            # 获取章节文本
            content = soup.select('#content')[0].text
            # 按照指定格式替换章节内容，运用正则表达式
            content = re.sub(r'\(.*?\)', '', content)
            content = re.sub(r'\r\n', '', content)
            content = re.sub(r'\n+', '\n', content)
            content = re.sub(r'<.*?>+', '', content)
            # 单独写入这一章
            with open(r'.\%s\%s %s.txt' % (self.title, self.num, subtitle), 'w', encoding='utf-8') as f:
                f.write(subtitle + content)
            f.close()
            print(self.num, subtitle, '下载成功')

        except Exception as e:
            print(e)
            # print(subtitle, '下载失败', self.url)
            # errorPath = '.\Error\%s' % (self.title)
            # # 创建错误文件夹
            # try:
            #     os.makedirs(errorPath)
            # except Exception as e:
            #     pass
            # # 写入错误文件
            # with open("%s\error_url.txt" % (errorPath), 'a', encoding='utf-8') as f:
            #     f.write(subtitle + "下载失败 " + self.url + '\n')
            # f.close()
        return


# 通过首页获得该小说的所有章节链接后下载这本书
def thread_getOneBook(indexUrl):
    soup = get_pages(indexUrl)
    # 获取书名
    title = soup.select('#chapter > div.chapterSo > div.chapName > strong')[0].text
    # 根据书名创建文件夹
    if title not in os.listdir('.'):
        os.mkdir(r".\%s" % (title))
        print(title, "文件夹创建成功———————————————————")

    # 加载此进程开始的时间
    print('下载 %s 的PID：%s...' % (title, os.getpid()))
    start = time.time()

    # 获取这本书的所有章节
    charts_url = []
    # 提取出书的每章节不变的url
    charts = soup.select("#chapter > div.chapterSo > div.chapterNum > ul > div.clearfix.dirconone > li")
    for i in charts:
        charts_url.append(i.select('a')[0]['href'])
    # 创建下载这本书的进程
    # p = multiprocessing.Pool()
    # 自己在下载的文件前加上编号，防止有的文章有上，中，下三卷导致有3个第一章
    num = 1
    for i in charts_url:
        #  p.apply_async(get_ChartTxt, args=(i, title, num))
        num += 1
        chart = get_ChartTxt(i, title, num)
        chart.run()
    print('等待 %s 所有的章节被加载......' % (title))
    # p.close()
    # p.join()
    end = time.time()
    print('下载 %s  完成，运行时间  %0.2f s.' % (title, (end - start)))
    print('开始生成 %s ................' % title)
    sort_allCharts(r'.', "%s.txt" % title)
    return


# 创建下载多本书书的进程
def process_getAllBook(base):
    # 输入你要下载的书的首页地址
    print('主程序的PID：%s' % os.getpid())
    book_index_url = [
        'http://www.quanshuwang.com/book/44/44683'
    ]
    print("-------------------开始下载-------------------")
    p = []
    for i in book_index_url:
        p.append(multiprocessing.Process(target=thread_getOneBook, args=(i,)))
    print("等待所有的主进程加载完成........")
    for i in p:
        i.start()
    for i in p:
        i.join()
    print("-------------------全部下载完成-------------------")

    return


# 合成一本书
def sort_allCharts(path, filename):
    lists = os.listdir(path)
    # 对文件排序
    # lists=sorted(lists,key=lambda i:int(re.match(r'(\d+)',i).group()))
    lists.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))
    # 删除旧的书
    if os.path.exists(filename):
        os.remove(filename)
        print('旧的 %s 已经被删除' % filename)
    # 创建新书
    with open(r'.\%s' % (filename), 'a', encoding='utf-8') as f:
        for i in lists:
            with open(r'%s\%s' % (path, i), 'r', encoding='utf-8') as temp:
                f.writelines(temp.readlines())
            temp.close()
    f.close()
    print('新的 %s 已经被创建在当前目录 %s ' % (filename, os.path.abspath(filename)))

    return


if __name__ == "__main__":
    # # 主页
    base = 'http://www.yznnw.com'
    # 下载指定的书
    process_getAllBook(base)
