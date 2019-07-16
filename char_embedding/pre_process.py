# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: pre_process.py
@time: 2019-07-12 13:07

这一行开始写关于本文件的说明与解释
"""

import os
import json


FILE_DIR = "../dataset/poetry/"
TRAIN_DIR = "./data/"

begin = "<BOS>"
end = "<EOS>"

# print(os.listdir(FILE_DIR))

def get_train_list(file_dir):
    """

    :param file_dir:
    :return:
    """
    train_list = []
    for file in os.listdir(file_dir):
        if ".json" in file:
            filepath = os.path.join(FILE_DIR,file)
            filelist = json.load(open(filepath))
            for fp in filelist:
                if "paragraphs" in fp:
                    for cell in fp["paragraphs"] :
                        clist = [begin]
                        clist.extend(list(cell))
                        clist.append(end)
                        train_list.extend(clist)
    print(len(train_list))
    return train_list


if __name__ == '__main__':
    trainlist = get_train_list(FILE_DIR)
    print(trainlist[:40])
    with open(os.path.join(TRAIN_DIR,"train_data.txt"),"w") as f:
        f.write(" ".join(trainlist))
    f.close()