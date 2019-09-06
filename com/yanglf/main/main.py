#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from removebg import RemoveBg

# https://www.remove.bg/profile#api-key
rmbg = RemoveBg("YOUR API-KEY", "error.log")
path = input("请输入路径:")
for pic in os.listdir(path):
    rmbg.remove_background_from_img_file('%s\%s' % (path, pic))
