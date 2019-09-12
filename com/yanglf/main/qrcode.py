#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MyQR import myqr

# words  二维码的内容   如果是   URL  扫码将会跳转
# picture  二维码背景图片
# colorized 背景图片是否彩色
myqr.run(words='http://www.baidu.com',
         picture='../img/20190907220124355.gif',
         colorized=True)
