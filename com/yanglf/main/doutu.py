# _*_coding:utf8_*_
# Project: spider
# File: main.py
# Author: ClassmateLin
# Email: 406728295@qq.com
# 有项目的可以滴滴我, Python/Java/PHP/Go均可。WX： ClassmateYue
# Time: 2020/2/21 4:54 下午
# DESC:
import requests
import os
from bs4 import BeautifulSoup


def get_html_text(url):
    """
    获取html文本
    :param url:
    :return:
    """
    return requests.get(url).text


def get_images_urls(html_text):
    """
    获取图片链接
    :param html_text:
    :return:
    """
    urls = []   # 保存提取的url列表
    soup = BeautifulSoup(html_text, 'html.parser')  # 创建一个soup对象，可以打印出来看看里面的内容
    div_tag = soup.find('div', {'id': 'post_content'})  # 查找id=post_content的标签
    img_tag_list = div_tag.find_all_next('img')  # 查找div下面的所有img标签
    for img_tag in img_tag_list[:-4]:  # 观察找到结果发现从倒数第四个开始并不是表情包，所以只迭代到倒数第四个
        url = img_tag.attrs['src']   # 提取img标题的src元素的值
        urls.append(url)
    return urls


def save_images(dir, urls):
    """
    保存图片
    :param urls:
    :return:
    """
    if not os.path.exists(dir):  # 使用os模块来判断文件夹是否存在，不存在则创建
        os.makedirs(dir)
    count = 1

    for url in urls:
        print('正在下载第{}张图片...'.format(str(count)))
        ext = url.split('.')[-1]  # 拿到图片的扩展名
        filename = dir + '/' + str(count) + '.' + ext  # 拼接图片的存储路径
        content = requests.get(url).content  # 通过GET请求获取图片的二进制内容，注意拿网页源码时候是text
        with open(filename, 'wb') as f:  # 已写二进制的形式打开文件
            f.write(content)  # 将图片内容写入
        count += 1   # count 用于图片命名和计数，递增1


if __name__ == '__main__':
    url = 'http://www.bbsnet.com/xiongmaoren-18.html'
    html_text = get_html_text(url)
    image_urls = get_images_urls(html_text)
    save_images('./images', image_urls)
