#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: pacman
@time: 2017/10/12 15:44
"""

import os
import json

from zhihu_oauth import ZhihuClient
from zhspider.settings import FILE_PATH
import traceback
import time
import random

TOKEN_FILE = FILE_PATH + '/token.pkl'

out_path = '{}/topictree.json'.format(FILE_PATH)

topic_url_fmt = 'https://www.zhihu.com/topic/{}/organize/entire'
root_id = 19776749


class TopicTree:
    client = ZhihuClient()

    def __init__(self):
        pass

    def login(self):
        if os.path.isfile(TOKEN_FILE):
            self.client.load_token(TOKEN_FILE)
        else:
            self.client.login_in_terminal(username='swuzhi@sina.com', password=self.getpass())
            self.client.save_token(TOKEN_FILE)

    def login_next(self):
        self.client.login_in_terminal(username='swuzhi@sina.com', password=self.getpass())

    def test(self):
        me = self.client.me()
        print('name', me.name)

    def get_topic(self, uid):
        topic = self.client.topic(uid)

        topic_dic = {}

        topic_dic['id'] = uid
        topic_dic['name'] = topic.name
        topic_dic['children'] = [{'id': item._id, 'name': item.name} for item in topic.children]

        with open(out_path, 'a', encoding='utf-8') as fw:
            json.dump(topic_dic, fw, ensure_ascii=False, sort_keys=True)
            fw.write('\n')

        for item in topic_dic['children']:
            cid = item['id']
            try:
                self.get_topic(cid)
                time.sleep(random.random())
            except Exception as e:
                traceback.print_exc()

                print('ban: ', cid)
                self.run(cid)

    def run(self, uid):
        self.login_next()
        self.get_topic(uid)

    def getpass(self):
        # with open('C:\\Users\\BaoQiang\\Desktop\\password.txt', 'r') as f:
        with open('/mnt/home/baoqiang/password.txt', 'r') as f:
            return f.read()


def tmp():
    print(random.random())


def main():
    topictree = TopicTree()
    topictree.run(root_id)


if __name__ == '__main__':
    # main()
    tmp()
