#!/usr/bin/env python
# encoding: utf-8

"""
@description: 从百度云下载的知乎话题数据，然后整理的数据文件

@author: pacman
@time: 2017/10/12 17:25
"""

import uuid
import os
from collections import defaultdict
import json
import traceback

input_path = 'C:\\Users\\BaoQiang\\Desktop\\zhihu-topic'
output_file = 'C:\\Users\\BaoQiang\\Desktop\\zhihu-topic.json'


def run():
    num = 0

    for filename in os.listdir(input_path):
        fullfile = os.path.join(input_path, filename)

        word_dict = defaultdict(list)
        ids = [-1 for _ in range(100)]

        with open(fullfile, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                try:
                    current_level = get_current(line)

                    line = line.strip()
                    # uid = str(uuid.uuid1())
                    num += 1
                    uid = num

                    # line = ''

                    if current_level != 0:
                        word_dict[ids[current_level - 1]].append({'id': uid, 'name': line})

                    ids[current_level] = '{}\t{}'.format(uid, line)

                except Exception as e:
                    traceback.print_exc()

        with open(output_file, 'a', encoding='utf-8') as fw:

            for key, value in word_dict.items():
                uid, name = process_key(key)
                json.dump({'id': uid, 'name': name, 'children': value}, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')


def process_key(key):
    attrs = key.split('\t')
    if len(attrs) != 2:
        return key, ''
    return attrs


def get_current(line):
    total = 0
    for item in line:
        if item == ' ':
            total += 1
        else:
            break

    if int(total / 4) != total / 4:
        raise ValueError('wrong space')
    else:
        return int(total / 4)


def main():
    run()


if __name__ == '__main__':
    main()
