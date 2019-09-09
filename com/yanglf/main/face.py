#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import base64

detect_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
merge_url = 'https://api-cn.faceplusplus.com/imagepp/v1/mergeface'
APK_KEY = 'hWhkHVmgzf66EYSDQGYAzJ5mWPjDUUo9'

API_SECRET = 'MwMht-dGxgyS1kLoRYDp60sLZIpN4DM6'

'''
人脸检测分析  ->  获取人脸关键点
'''


def detect_face(image_base64):
    data = {
        'api_key': APK_KEY,
        'api_secret': API_SECRET,
        'image_base64': image_base64
    }
    detect_response = requests.post(detect_url, data=data)
    json_text = detect_response.json()
    print(json_text)
    face_rectangle = json_text['faces'][0]['face_rectangle']
    return face_rectangle


'''
人脸融合
'''


def merge_face(template_base64,
               template_rectangle,
               merge_base64,
               merge_rectangle,
               merge_rate,
               target_img=r'D:\壁纸\美女\merge.jpg'):
    data = {
        'api_key': APK_KEY,
        'api_secret': API_SECRET,
        'template_base64': template_base64,
        'template_rectangle': template_rectangle,
        'merge_base64': merge_base64,
        'merge_rectangle': merge_rectangle,
        'merge_rate': merge_rate
    }
    merge_repo = requests.post(merge_url, data=data)
    merge_json = merge_repo.json()
    result = merge_json['result']
    img_data = base64.b64decode(result)
    file = open(target_img, 'wb')
    file.write(img_data)
    file.close()


f = open(r'D:\壁纸\美女\a88959a4-ae9f-11e9-b0ce-00155d6c7dc5.jpg', 'rb')
image1 = base64.b64encode(f.read())
f.close()
ff1 = detect_face(image1)
rectangle1 = str(str(ff1['top']) + "," + str(ff1['left']) + "," + str(ff1['width']) + "," + str(ff1['height']))
f = open(r'D:\壁纸\美女\adbe9388-ae9f-11e9-a21b-00155d6c7dc5.jpg', 'rb')
image2 = base64.b64encode(f.read())
f.close()
ff2 = detect_face(image2)
rectangle2 = str(str(ff2['top']) + "," + str(ff2['left']) + "," + str(ff2['width']) + "," + str(ff2['height']))
merge_face(image1, rectangle1, image2, rectangle2, 50)
