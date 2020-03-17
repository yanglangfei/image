import requests
import time
import json
import os
import threading


class HonorSkin(threading.Thread):
    def __init__(self, name):
        super(HonorSkin, self).__init__()
        self.name = name
        self.hero_json_url = "http://pvp.qq.com/web201605/js/herolist.json"
        self.hero_skin_base_url = "http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
        }

    def parser_url(self, url):
        """ 解析网址
        :param url: 网址
        :return: 网址响应内容
        """
        print(url)
        response = requests.get(url, headers=self.headers)
        return response.content

    def get_content_list(self, json_str):
        """ 通过json数据，转为字典数据
        :param json_str:
        :return:
        """
        dict_ret = json.loads(json_str)
        return dict_ret

    def save_content_list(self, path, content_list):
        """ 将 json 数据写入文件
        :param path: 地址
        :param content_list: 列表数据
        """
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content_list, f, ensure_ascii=False, indent=4)
        print("保存成功")

    def load_hero_list(self, path):
        """ 加载英雄列表文件数据
        :param path: 文件路径
        :return: 英雄列表字典数据
        """
        hero_list = {}
        with open(path, "r", encoding="utf-8") as f:
            heros_str = f.read()
            if heros_str.startswith(u'\ufeff'):  # 避免报错json.decoder.JSONDecodeError
                heros_str = heros_str.encode('utf8')[3:].decode('utf8')

            hero_list = json.loads(heros_str, encoding="utf-8")

        return hero_list

    def save_skin(self, path, skin):
        """ 保存英雄皮肤数据
        :param path: 保存地址
        :param skin: 皮肤数据
        """
        with open(path, "wb") as f:
            f.write(skin)
        print("皮肤保存成功：" + path)

    def parse_hero_list_save_skin(self, content_list, save_path):
        """ 解析英雄列表数据，以及保存皮肤
        :param content_list: 英雄列表数据
        :param save_path: 保存路径
        :return: 返回保存皮肤总数
        """
        hero_skin_counter = 0
        for content in content_list:
            ename = content["ename"]
            cname = content["cname"]
            skin_names = content["skin_name"].split('|')
            skin_amount = len(skin_names)
            for skin_num in range(1, skin_amount + 1):  # 因为左闭右开，所以数量 +1
                skin_url = self.hero_skin_base_url.format(ename, ename, skin_num)
                skin = self.parser_url(skin_url)
                skin_name = cname + "-" + skin_names[skin_num - 1] + ".jpg"
                self.save_skin(save_path + skin_name, skin)
                hero_skin_counter += 1

        return hero_skin_counter

    def run(self):

        # 计时和设置保存目录
        time_start_count = time.time()
        hero_skin_dir = "D:\\HonorSkins\\"
        if not os.path.exists(hero_skin_dir):
            os.mkdir(hero_skin_dir)

        # 发请求，获取英雄json列表，并保存
        hero_json_str = self.parser_url(self.hero_json_url)
        hero_list = self.get_content_list(hero_json_str)
        self.save_content_list(hero_skin_dir + "HonorHeroList.txt", hero_list)

        # 临时步骤 读取保存的数据(因为目前马超数有缺失，如你此时下载数据没有可以忽略)
        # hero_list = self.load_hero_list(hero_skin_dir + "HonorHeroList.txt")
        # print(type(hero_list))
        # print(hero_list)
        # for content in hero_list:
        #     print(type(content))
        #     print(content)

        # 解析英雄json列表，拼凑皮肤地址，发请求，下载皮肤
        hero_skin_counter = self.parse_hero_list_save_skin(hero_list, hero_skin_dir)

        time_finish_count = time.time()
        time_spend = time_finish_count - time_start_count
        print("总共下载 " + str(hero_skin_counter) + " 张皮肤，耗时 " + str(time_spend) + "s")


if __name__ == "__main__":
    honor_skin = HonorSkin("t1")
    honor_skin.start()
