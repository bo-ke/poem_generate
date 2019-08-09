# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: api_poem_generate.py
@time: 2019-07-24 16:39

这一行开始写关于本文件的说明与解释
"""
from generation.generate import test

def api_generate(name1,name2):
    res = test(boy_name=name1, girl_name=name2)
    return res


if __name__ == '__main__':
    print(api_generate("唐梅芝","胡歌"))
    print(api_generate("李鸿斌","程萌"))
    print(api_generate("张立","胡妍"))
    print(api_generate("张一山","杨紫"))