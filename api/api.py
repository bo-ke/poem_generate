# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: api.py
@time: 2019-07-24 15:29

这一行开始写关于本文件的说明与解释
"""
from create_name import api_make_name
from src import api_match_name




if __name__ == '__main__':
    name = "张立"
    name2,score = api_match_name(name)
    name_child = api_make_name(name,name2,is_girl=True)
    print(name2,score)
    print(name_child)